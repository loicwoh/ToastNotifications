# Reprise dans LabVIEW

Branche : `feature/toastapi-contracts-content`.

## Point d'entrée

Ouvrir `ToastAPI.lvproj`, puis `Examples/Build Reply Content.vi`.
Le diagramme enchaîne les méthodes publiques d'ajout, `Validate`, puis `Read Data`.
Les entrées préremplies décrivent un toast Reply. L'exemple construit uniquement les données : aucune notification Windows n'est affichée.

Pour la revue manuelle, examiner les valeurs des entrées, le snapshot `Content Data` et `error out`.
On peut par exemple modifier l'identifiant du champ sans modifier celui du bouton pour observer l'erreur d'association, ou vider le texte.

## Vérification effectuée

Les onze méthodes de classe et le VI d'exemple ont été contrôlés avec `Execution:State = eIdle` : ils sont chargeables et exécutables dans LabVIEW 2026.
Les diagrammes de l'exemple et de la validation ont été rendus et examinés.
Les connecteurs des méthodes créées utilisent le pattern 4815 et les paramètres de classe ont été vérifiés dans les fichiers enregistrés.
Les liens de typedef des paramètres et des éléments des tableaux ont été contrôlés.
Le projet historique et ses fichiers versionnés n'ont pas été modifiés.

Aucun test unitaire n'est livré. Ces vérifications ne constituent pas une validation du comportement par exécution, ni une mesure de fuite mémoire.
Le backend .NET/WinRT, les notifications et les callbacks ne sont pas implémentés dans cette tranche.

## Points à relire ensemble

- Noms et connecteurs de l'API ; granularité des méthodes `Add`.
- Chaîne d'arguments opaque du bouton et tableau clé/valeur pour le corps.
- Règles de validation et messages d'erreur.
- Contrat de `Handle Activation`, propriété des références et fermeture décrits dans `ARCHITECTURE.md`.

Enregistrer les VIs avant de rendre la main. Les modifications se poursuivent sur cette branche jusqu'à la revue et la fusion.
