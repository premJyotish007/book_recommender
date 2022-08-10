# Cram Your Jam

<hr>
Book recommendation algorithm that relies on a user's song playlist to make accurate suggestions for next books to read.

As two mediums of expressions inherently tied to the same emotional stimulator: text/lyrics, the choice of your songs can reveal a lot about what books you might be interested in, through the song pace, its genres, any specific themes and/or nouns associated with it, and so on.

Current progress: Have set up an API infrastructure to make REST API calls to the spotify api for song properties, a song lyrics scraper, and the google books api to accumulate data about books, their description, categories, and themes. This obtained data serves to represent as many genres and as many varations of choices possible among listeners. Furthermore, this training data would be used to train a combination of machine learning algorithms such as neural network, decision trees, and other graph algorithms to make the most relevant recommendations.
