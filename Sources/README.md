# ToastAPI

Bibliothèque LabVIEW 2026 pour construire, afficher et recevoir les réponses des notifications Windows via Microsoft.Toolkit.Uwp.Notifications.
Ouvrir `ToastAPI.lvproj`, puis `Examples/Build Toast With Classes.vi`. Le projet historique et son PoC sont conservés dans `Archive/ToastNotifications.lvproj` et `Archive/SandBox`.

## Utilisation

1. Créer un `ToastBuilder` avec `Create`, puis appeler `Add Text`.
2. Ajouter un champ avec `Add Text Input` : `id` identifie la valeur renvoyée au callback ; `Title` et `Placeholder Text` règlent sa présentation.
3. Ajouter `Add Bouton` : `Content` est le libellé affiché et `Arguments` la chaîne renvoyée à l'activation.
4. Lire éventuellement le XML avec `Get XML`.
5. Appeler `ToastService.Initialize`, puis `Register For Events` avec le gestionnaire injecté, avant `Show`.
6. Attendre l'interaction utilisateur. Fermer les ressources après la fin de cette attente.

L'exemple fournit un champ `Reply` et un bouton `Répondre` avec l'argument `action=Reply`. Saisir un texte puis cliquer sur ce bouton. Le gestionnaire de base affiche le payload LabVIEW en JSON ; fermer son dialogue puis appuyer sur Stop pour terminer l'exemple.
Les textes affichés ne deviennent pas automatiquement des arguments d'activation.

Pour changer la réaction, créer une classe enfant d'`ActivationHandler`, surcharger `Handle Activation` et passer cette instance à `Register For Events`. Les données reçues sont des chaînes et des paires clé/valeur LabVIEW ; aucune référence .NET n'est exposée au gestionnaire.

## Organisation sur disque

| Dossier | Contenu |
|---|---|
| ToastNotification | Bibliothèque principale, Activation.ctl et Argument.ctl |
| ToastBuilder | Classe de composition, méthodes, accesseurs et typedef de référence |
| ToastService | Classe du service, enregistrement et conversion des activations |
| ActivationHandler | Classe du point d'extension à dispatch dynamique |
| Toast Native | Bibliothèque des appels natifs du toolkit et ses membres |
| Reflection DotNet | Bibliothèque des helpers génériques de réflexion et de nettoyage |
| Examples | Exemples avec classes et appels natifs directs |

Chaque classe ou bibliothèque et ses membres occupent un dossier plat. Les dossiers virtuels de scope restent indépendants de cette organisation physique.
La DLL du toolkit reste sous `bins`. Une copie identique dans `Archive/bins` conserve les chemins relatifs du prototype historique. Les exports, sondes et captures de travail restent dans `_review` à la racine du dépôt, hors versionnement.

## Références et fermeture

Le builder possède son handle natif. Ses copies partagent ce handle : un seul propriétaire doit appeler `Close` après le dernier usage. Les accesseurs et sorties `reference out` ne créent pas une nouvelle acquisition.
Le service possède son enregistrement de callback et sa référence native. `Close` désenregistre avant de fermer cette référence ; le builder emprunté doit être fermé séparément.

Les conversions ferment leurs références temporaires, y compris les métadonnées de réflexion et les énumérateurs. Les arguments fournis par le callback restent empruntés.
L'exemple appelle `System.GC.Collect()` après les fermetures : une collecte ponctuelle a fait passer le callback resté réservé de `eRunning` à `eIdle` sur ce poste, sans quitter LabVIEW. Cet appel n'est pas placé dans le callback et ne prouve pas l'absence de fuites.

## Validation et limites de la première phase

- Construction, affichage, activation du bouton et capture de saisie validés manuellement pendant le développement.
- 49 VIs vérifiés exécutables après la réorganisation, sans réémettre automatiquement de notification.
- Aides contextuelles des VIs, contrôles, classes, bibliothèques et projet renseignées.
- Aucun framework de tests unitaires ni dépendance Caraya ajouté.

Le gestionnaire de démonstration bloque le callback pendant son dialogue. La protection contre les doubles enregistrements, l'attente bornée des callbacks en cours et les mesures de stabilité mémoire restent à traiter. La gestion systématique des références temporaires de composition, notamment du bouton créé par `Add Bouton`, demande encore une passe dédiée.

Voir [ARCHITECTURE.md](ARCHITECTURE.md), [CALLBACK-LIFETIME.md](CALLBACK-LIFETIME.md) et [HANDOFF.md](HANDOFF.md).
