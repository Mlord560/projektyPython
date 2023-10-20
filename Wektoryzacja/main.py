import labels as labels
import torch
from transformers import BertTokenizer, BertModel
import logging
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

sentences = [
    "After stealing money from the bank vault, the bank robber was seen fishing on the Mississippi river bank.",
    "The time elapsed the day at the river bank."]

sent = sentences[0]

encoded = tokenizer.encode_plus(
    text=sent,  # the sentence to be encoded
    add_special_tokens=True,  # Add [CLS] and [SEP]
    truncation=True,
    padding=True,  # Add [PAD]s
    return_attention_mask=True,  # Generate the attention mask
    return_tensors='pt',  # ask the function to return PyTorch tensors
)

input_ids = encoded['input_ids']
attn_mask = encoded['attention_mask']

print(input_ids)
print(attn_mask)

# Load pre-trained model (weights)
model = BertModel.from_pretrained('bert-base-uncased',
                                  output_hidden_states=True,  # Whether the model returns all hidden-states.
                                  )

# Put the model in "evaluation" mode, meaning feed-forward operation.
model.eval()

# Run the text through BERT, and collect all the hidden states produced
# from all 12 layers.
with torch.no_grad():
    outputs = model(input_ids, attn_mask)

    # Evaluating the model will return a different number of objects based on
    # how it's  configured in the `from_pretrained` call earlier. In this case,
    # becase we set `output_hidden_states = True`, the third item will be the
    # hidden states from all layers. See the documentation for more details:
    # https://huggingface.co/transformers/model_doc/bert.html#bertmodel
    hidden_states = outputs[2]

print("Number of layers:", len(hidden_states), "  (initial embeddings + 12 BERT layers)")
layer_i = 0

print("Number of batches:", len(hidden_states[layer_i]))
batch_i = 0

print("Number of tokens:", len(hidden_states[layer_i][batch_i]))
token_i = 0

print("Number of hidden units:", len(hidden_states[layer_i][batch_i][token_i]))

# For the 5th token in our sentence, select its feature values from layer 5.
# token_i = 5
# layer_i = 5
# vec = hidden_states[layer_i][batch_i][token_i]

# Plot the values as a histogram to show their distribution.
# plt.figure(figsize=(10,10))
# plt.hist(vec, bins=200)
# plt.show()

# Concatenate the tensors for all layers. We use `stack` here to
# create a new dimension in the tensor.
token_embeddings = torch.stack(hidden_states, dim=0)

token_embeddings.size()

# Remove dimension 1, the "batches".
token_embeddings = torch.squeeze(token_embeddings, dim=1)

token_embeddings.size()

# Swap dimensions 0 and 1.
token_embeddings = token_embeddings.permute(1, 0, 2)

print(f'Tokens, layers, features: {token_embeddings.size()}')

# Stores the token vectors, with shape [14 x 3,072]
token_vecs_cat = []

# `token_embeddings` is a [14 x 12 x 768] tensor.

# For each token in the sentence...
for token in token_embeddings:
    # `token` is a [14 x 768] tensor

    # Concatenate the vectors (that is, append them together) from the last
    # four layers.
    # Each layer vector is 768 values, so `cat_vec` is length 3072.
    cat_vec = torch.cat((token[-1], token[-2], token[-3], token[-4]), dim=0)

    # Use `cat_vec` to represent `token`.
    token_vecs_cat.append(cat_vec)

for i, token_str in enumerate(tokenizer.convert_ids_to_tokens(input_ids[0])):
    print(i, token_str)


print('Shape is: %d x %d' % (len(token_vecs_cat), len(token_vecs_cat[0])))
print(token_vecs_cat)

print('First 5 vector values for each instance of "bank".')
print('')
print("bank vault   ", str(token_vecs_cat[6][:5]))
print("bank robber  ", str(token_vecs_cat[10][:5]))
print("river bank   ", str(token_vecs_cat[19][:5]))

# Calculate the cosine similarity between the word bank
# in "bank robber" vs "river bank" (different meanings).
diff_bank = 1 - cosine(token_vecs_cat[10], token_vecs_cat[19])

# Calculate the cosine similarity between the word bank
# in "bank robber" vs "bank vault" (same meaning).
same_bank = 1 - cosine(token_vecs_cat[10], token_vecs_cat[6])

print('Vector similarity for  *similar*  meanings:  %.2f' % same_bank)
print('Vector similarity for *different* meanings:  %.2f' % diff_bank)