# PWA - Audio Transcription App

Votre application web a maintenant été transformée en PWA (Progressive Web App) ! 🎉

## Fonctionnalités PWA ajoutées

### ✅ Installation native
- L'application peut maintenant être installée sur mobile et desktop
- Bouton d'installation automatique qui apparaît
- Icône sur l'écran d'accueil / bureau

### ✅ Fonctionnement hors ligne
- Service Worker configuré
- Cache automatique des ressources
- Fonctionnement même sans connexion internet

### ✅ Mises à jour automatiques
- Notification automatique des nouvelles versions
- Installation des mises à jour en arrière-plan

### ✅ Interface native
- Affichage en plein écran (sans barre d'adresse)
- Splashscreen automatique
- Thème adapté au système

## Comment tester votre PWA

### 1. En développement
```bash
npm run dev
```
Puis ouvrez Chrome/Edge et allez dans les DevTools > Application > Manifest

### 2. En production
```bash
npm run build
npm run preview
```

### 3. Test d'installation
- Sur mobile : "Ajouter à l'écran d'accueil"
- Sur desktop : icône d'installation dans la barre d'adresse

## Personnaliser vos icônes

Pour remplacer les icônes temporaires par votre icône personnalisée :

```bash
node replace-icon.js path/to/your/icon.png
npm run build
```

## Configuration PWA

La configuration se trouve dans `vite.config.ts` :
- **Nom de l'app** : "Audio Transcription App"
- **Nom court** : "AudioTranscribe"
- **Couleur thème** : #1db584
- **Mode d'affichage** : standalone

## Fichiers PWA générés

- `manifest.webmanifest` - Configuration de l'app
- `sw.js` - Service Worker
- `pwa-*` - Icônes de différentes tailles
- `apple-touch-icon.png` - Icône iOS
- `browserconfig.xml` - Configuration Windows

## Déploiement

Votre PWA est prête pour le déploiement ! Les fichiers dans `/dist` contiennent tout le nécessaire.

## Support navigateurs

✅ Chrome/Edge (Android/Desktop)  
✅ Safari (iOS/macOS)  
✅ Firefox (Android/Desktop)  
✅ Samsung Internet  

---

*Votre webapp est maintenant une vraie PWA ! 🚀*