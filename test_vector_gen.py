
import os
from dotenv import load_dotenv,find_dotenv

# Find the .env file
dotenv_path = find_dotenv()
output = load_dotenv(dotenv_path, override=True)


from app.tasks.chunk_gen import get_char_text_chunks
from app.tasks.embed_gen import build_MiniLM_embeddings, build_googleai_embeddings, build_openai_embeddings


text = """
Most machine learning models are used to make predictions. Discriminative algorithms try to classify input data given some set of features and predict a label or a class to which a certain data example belongs.

Say, we have training data that contains multiple images of cats and guinea pigs. They are also called samples. Each sample has input features (X) and output class labels (Y). And we also have a neural net to look at the image and tell whether it’s a guinea pig or a cat, paying attention to the features that distinguish them.

Discriminative modeling 

Discriminative modeling

Let’s limit the difference between cats and guinea pigs to just two features x (for example, “the presence of the tail” and “the size of the ears”). Since each feature is a dimension, it’ll be easy to present them in a 2-dimensional data space. In the viz above, the blue dots are guinea pigs and the red dots are cats. The line depicts the decision boundary or that the discriminative model learned to separate cats from guinea pigs based on those features.

When this model is already trained and used to tell the difference between cats and guinea pigs, it, in some sense, just “recalls” what the object looks like from what it has already seen.

So, if you show the model an image from a completely different class, for example, a flower, it can tell that it’s a cat with some level of probability. In this case, the predicted output (ŷ) is compared to the expected output (y) from the training dataset. Based on the comparison, we can figure out how and what in an ML pipeline should be updated to create more accurate outputs for given classes.

To recap, the discriminative model kind of compresses information about the differences between cats and guinea pigs, without trying to understand what a cat is and what a guinea pig is.

Generative modeling
Generative algorithms do the complete opposite — instead of predicting a label given to some features, they try to predict features given a certain label. Discriminative algorithms care about the relations between x and y; generative models care about how you get x.

Generative modeling 

Generative modeling

Mathematically, generative modeling allows us to capture the probability of x and y occurring together. It learns the distribution of individual classes and features, not the boundary.

Getting back to our example, generative models help answer the question of what is the "cat itself" or "guinea pig itself.” The viz shows that a generative model can predict not only all the tail and ear features of both species but also other features from a class. This means it learns features and their relations to get an idea of what those animals look like in general.

And if the model knows what kinds of cats and guinea pigs there are in general, then their differences are also known. Such algorithms can learn to recreate images of cats and guinea pigs, even those that were not in the training set.

A generative algorithm aims for a holistic process modeling without discarding any information. You may wonder, “Why do we need discriminative algorithms at all?” The fact is that often a more specific discriminative algorithm solves the problem better than a more general generative one.

But still, there is a wide class of problems where generative modeling allows you to get impressive results. For example, such breakthrough technologies as GANs and transformer-based algorithms.

Generative Adversarial Networks
A generative adversarial network or GAN is a machine learning algorithm that puts the two neural networks — generator and discriminator — against each other, hence the “adversarial” part. The contest between two neural networks takes the form of a zero-sum game, where one agent's gain is another agent's loss.

GANs were invented by Jan Goodfellow and his colleagues at the University of Montreal in 2014. They described the GAN architecture in the paper titled “Generative Adversarial Networks.” Since then, there has been a lot of research and practical applications, making GANs the most popular generative AI model.

"""



print("#"*24)
print("generate chunks")
chunks = get_char_text_chunks(text, 256, 16)
print("generate vectors")
# Embed chunks
for idx, vector in build_googleai_embeddings(chunks):
# for idx, vector in build_openai_embeddings(chunks):
# for idx, vector in build_MiniLM_embeddings(chunks):
    print("idx: "+ str(idx))
    print("vector: "+ str(len(vector)))