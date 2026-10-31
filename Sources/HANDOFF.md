# Reprise dans LabVIEW

Ouvrir `ToastAPI.lvproj`, puis `Examples/Build Toast With Classes.vi`.
La première phase fournit le wrapper direct, un champ Reply, un bouton Répondre, l'enregistrement OnActivated, la conversion des données et le handler à dispatch dynamique injecté.

Saisir un texte et cliquer sur Répondre ; le handler de base affiche Arguments et User Inputs en JSON. Fermer le dialogue puis appuyer sur Stop. Le service est désenregistré et fermé, puis le builder fermé. Une collecte .NET termine l'exemple pour libérer la réservation du callback constatée sur ce poste.

Les dossiers physiques sont plats : ToastNotification, ToastBuilder, ToastService, ActivationHandler, Toast Native, Reflection DotNet, Examples et Support. Chaque classe ou bibliothèque est placée avec ses membres. Les scopes restent des dossiers virtuels.
Les aides contextuelles décrivent les paramètres et la propriété des handles. Les documents README, ARCHITECTURE et CALLBACK-LIFETIME décrivent le comportement actuel.

Les interactions Windows ont été validées manuellement par l'utilisateur. Les 50 VIs sont exécutables après déplacement et sauvegarde des liens. Aucun framework de tests unitaires n'est ajouté.

Suite du travail : durcir la fermeture et les doubles enregistrements, organiser l'attente des callbacks en cours, fermer systématiquement les temporaires de composition et mesurer la mémoire sur des activations répétées. Le dialogue du handler de base est un outil de démonstration ; un handler applicatif devrait transférer les données vers sa propre boucle.

Enregistrer avant de rendre la main. Le prototype historique et SandBox restent conservés sous `Archive`, avec leurs dépendances. `_review` est ignoré par Git et ne constitue pas une dépendance du projet.
