Bienvenue dans ce projet du Bloc n°5 de la de la certification Jedha !...
 - Projet Get Around - 

Nom : DINE Aloïs Jesshuan
Mail : jesshuan.dine@gmail.com

Lien vidéo de la présentation :
https://shar

-----

THREE FOLDERS :

- Streamlit_app : the analysis on the impact of the new feature of managment of the user delay. The notebook 'eda_for_analysis' allows to make the analysis step by step, with arguments and choices... The app.py is the construction file of the Streamlit app.

- Prediction_model_MLFlow2 : 


DEPLOIEMENT

Pour faire tourner le notebook dans un environnement Jupyter Lab doté de Tensorflow GPU, utiliser l'image Docker fournie :

- s'assurer que Docker soit démarré

- depuis ce répertoire, dans un terminal : ``` docker-compose up ```

- se rendre à l'adresse http indiquée (le token est inclu dans l'adresse)


-----

CREDITS

Pour les modèles pré-entrainés

DistilBERT : Victor Sanh, Lysandre Debut, Julien Chaumond et Thomas Wolf (paper : https://arxiv.org/abs/1910.01108)

DistilBERT_SMSSPAM_Classifier : Manirathinam21 (page Hugging Face : https://huggingface.co/Manirathinam21/DistilBert_SMSSpam_classifier)