import sharp from 'sharp';
import fs from 'fs';
import path from 'path';

// Usage: node replace-icon.js <path-to-your-icon>
// Example: node replace-icon.js ./my-microphone-icon.png

async function replaceIcons(iconPath) {
  if (!iconPath) {
    console.error('Veuillez fournir le chemin vers votre icône');
    console.log('Usage: node replace-icon.js <path-to-your-icon>');
    process.exit(1);
  }

  if (!fs.existsSync(iconPath)) {
    console.error('Le fichier icône n\'existe pas:', iconPath);
    process.exit(1);
  }

  console.log('Génération des icônes PWA à partir de:', iconPath);

  const sizes = [
    { size: 64, name: 'pwa-64x64.png' },
    { size: 192, name: 'pwa-192x192.png' },
    { size: 512, name: 'pwa-512x512.png' },
    { size: 512, name: 'maskable-icon-512x512.png' },
    { size: 180, name: 'apple-touch-icon.png' },
    { size: 32, name: 'favicon.ico' }
  ];

  try {
    for (const { size, name } of sizes) {
      await sharp(iconPath)
        .resize(size, size)
        .png()
        .toFile(path.join('./public', name));
      
      console.log(`✓ Généré ${name}`);
    }

    console.log('\n🎉 Toutes les icônes PWA ont été générées avec succès!');
    console.log('Vous pouvez maintenant builder votre application avec: npm run build');
  } catch (error) {
    console.error('Erreur lors de la génération des icônes:', error.message);
    process.exit(1);
  }
}

const iconPath = process.argv[2];
replaceIcons(iconPath);