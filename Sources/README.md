# ToastAPI

Bibliothèque LabVIEW 2026 pour construire, afficher et recevoir les réponses des notifications Windows via Microsoft.Toolkit.Uwp.Notifications.
Ouvrir `ToastAPI.lvproj`, puis `Examples/Build Toast With Classes.vi`. Le projet historique et son PoC sont conservés dans `Archive/ToastNotifications.lvproj` et `Archive/SandBox`.

## Utilisation

1. Créer un `ToastBuilder` avec `Create`, puis appeler `Add Text`.
2. Ajouter un champ avec `Add Text Input` : `id` identifie la valeur renvoyée au callback ; `Title` et `Placeholder Text` règlent sa présentation.
3. Ajouter `Add Bouton` : `Content` est le libellé affiché et `Arguments` la chaîne renvoyée à l'activation.
4. Lire éventuellement le XML avec `Get XML`.
5. Appeler `ToastService.Initialize` avec le gestionnaire injecté. Récupérer le handler initialisé si nécessaire, préparer sa réception côté application, puis appeler `ToastService.Register For Events` avant `Show`.
6. Attendre l'interaction utilisateur. Fermer les ressources après la fin de cette attente.

L'exemple fournit un champ `Reply` et un bouton `Répondre` avec l'argument `action=Reply`. Le gestionnaire de base est désormais sans action : pour exploiter ou afficher la réponse, utiliser un gestionnaire dérivé. Appuyer sur Stop pour terminer l'exemple.
Les textes affichés ne deviennent pas automatiquement des arguments d'activation.

Pour changer la réaction, créer une classe enfant d'`ActivationHandler`, surcharger `Handle Activation` et passer cette instance à `ToastService.Initialize`. Les hooks `Initialize` et `Close` permettent au handler de gérer ses ressources. Le service conserve le handler initialisé et l'utilise lors de `Register For Events`. Les données reçues sont des chaînes et des paires clé/valeur LabVIEW ; aucune référence .NET n'est exposée au gestionnaire.

## Plusieurs actions et User Event

`Examples/Toast With Multiple Actions.vi` utilise `UserEventActivationHandler` pour transmettre les activations à une boucle Event Structure. Les boutons **Accept** et **Reject** portent leurs propres arguments ; `Set Activation Arguments` configure ceux du corps du toast, avec l'activation Foreground. Les trois chaînes incluent `requestId=42` et une action distincte.

Le handler crée son User Event dans `Initialize` et le détruit dans `Close`. L'exemple récupère la référence sur le handler initialisé et possède son propre enregistrement d'événement. Le payload comporte `Activation` et `error`. Sans champ de saisie, `Activation.User Inputs` est normalement vide : les actions sont dans `Activation.Arguments`.

Voir le [guide détaillé](Examples/Multiple%20Actions.md) pour le câblage, la procédure d'essai et les vérifications restantes du handler (#22) et du cycle de vie (#16).

## Réponse texte

Pour un exemple de saisie dont le résultat est visible dans la boucle LabVIEW, ouvrir `Examples/Toast With Reply.vi`. Le champ `Reason` et le bouton **Send** transmettent le texte dans `Activation.User Inputs` ; `action=reject&requestId=42` reste dans `Activation.Arguments`. La réception de la clé `Reason` et de la valeur saisie a été confirmée par les captures de l'utilisateur. Voir le [guide de réponse texte](Examples/Reply%20Input.md), qui distingue le fonctionnement validé des essais restant à réaliser. Le bouton est actuellement affiché sous le champ, sans association visuelle inline explicite.

## Bouton ouvrant un lien

`ToastBuilder.Add Link Button` ajoute un bouton avec deux chaînes : `Content` pour le texte affiché et `URl` pour l'adresse à ouvrir. Il utilise l'activation `Protocol` de Windows ; le clic sur ce bouton ouvre l'application associée à l'URI au lieu d'appeler le handler LabVIEW. Le clic sur le corps du toast est une activation distincte.

Ouvrir `Examples/Toast With Link Button.vi`, lancer le VI et cliquer sur **Open project on GitHub**. Le lien utilisé est `https://github.com/loicwoh/ToastNotifications`. Appuyer ensuite sur **stop** dans LabVIEW pour libérer le service et le builder. Les valeurs sont des constantes sur le diagramme ; `Toast XML` expose le contenu sérialisé. L'exemple attend Stop même si la préparation retourne une erreur.

Voir le [guide de l'exemple](Examples/Protocol%20Activation.md) et l'[index des exemples](Examples/README.md). L'ouverture du lien a été validée manuellement par l'utilisateur.

## Organisation sur disque

| Dossier | Contenu |
|---|---|
| ToastNotification | Bibliothèque principale, Activation.ctl et Argument.ctl |
| ToastBuilder | Classe de composition, méthodes, accesseurs et typedef de référence |
| ToastService | Classe du service, enregistrement et conversion des activations |
| ActivationHandler | Classe du point d'extension à dispatch dynamique |
| Toast Native | Bibliothèque des appels natifs du toolkit et ses membres |
| Reflection DotNet | Bibliothèque des helpers génériques de réflexion et de nettoyage |
| PlugIns/UserEventActivationHandler | Handler concret, méthodes de cycle de vie, référence d'événement et typedef du payload |
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

Le gestionnaire de base n'effectue aucune action ; le handler applicatif doit retourner rapidement. La protection contre les doubles enregistrements, l'attente bornée des callbacks en cours et les mesures de stabilité mémoire restent à traiter. La gestion systématique des références temporaires de composition, notamment du bouton créé par `Add Bouton`, demande encore une passe dédiée. `Add Link Button` utilise une surcharge directe du builder et n'acquiert pas ce handle temporaire de bouton.

Voir [ARCHITECTURE.md](ARCHITECTURE.md), [CALLBACK-LIFETIME.md](CALLBACK-LIFETIME.md) et [HANDOFF.md](HANDOFF.md).
