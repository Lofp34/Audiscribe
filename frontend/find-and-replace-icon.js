import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function findAndReplaceIcon() {
  console.log('🔍 Recherche de votre icône...');
  
  // Chemins possibles à vérifier
  const searchPaths = [
    '../Untitled design.png',
    '../untitled design.png',
    '../Untitled_design.png', 
    '../untitled_design.png',
    './Untitled design.png',
    './untitled design.png'
  ];
  
  // Chercher aussi tous les fichiers PNG dans le dossier parent
  try {
    const parentDir = path.join(__dirname, '..');
    const files = fs.readdirSync(parentDir);
    const pngFiles = files.filter(file => 
      file.toLowerCase().endsWith('.png') && 
      file.toLowerCase().includes('untitled')
    );
    
    for (const file of pngFiles) {
      searchPaths.push(path.join('..', file));
    }
  } catch (err) {
    console.log('Impossible de lire le dossier parent');
  }

  let iconPath = null;
  
  // Tester chaque chemin possible
  for (const testPath of searchPaths) {
    const fullPath = path.resolve(__dirname, testPath);
    if (fs.existsSync(fullPath)) {
      iconPath = fullPath;
      console.log(`✅ Icône trouvée : ${testPath}`);
      break;
    }
  }

  if (!iconPath) {
    console.error('❌ Icône non trouvée !');
    console.log('Fichiers PNG trouvés dans le projet :');
    
    // Lister tous les PNG du projet
    try {
      const allPngs = [];
      function findPngs(dir) {
        const files = fs.readdirSync(dir);
        for (const file of files) {
          const fullPath = path.join(dir, file);
          if (fs.statSync(fullPath).isDirectory() && !file.includes('node_modules')) {
            findPngs(fullPath);
          } else if (file.toLowerCase().endsWith('.png')) {
            allPngs.push(fullPath);
          }
        }
      }
      
      findPngs(path.join(__dirname, '..'));
      allPngs.forEach(png => console.log(`  - ${path.relative(__dirname, png)}`));
      
    } catch (err) {
      console.log('Erreur lors de la recherche des PNG');
    }
    
    console.log('\nVeuillez vous assurer que votre icône :');
    console.log('1. Est bien dans le dossier racine du projet');
    console.log('2. S\'appelle exactement "Untitled design.png"');
    console.log('3. Ou utilisez : node replace-icon.js path/to/your/icon.png');
    return;
  }

  console.log('🎨 Génération des icônes PWA...');

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
        .resize(size, size, { 
          fit: 'contain',
          background: { r: 255, g: 255, b: 255, alpha: 0 }
        })
        .png()
        .toFile(path.join(__dirname, 'public', name));
      
      console.log(`✓ Généré ${name}`);
    }

    // Copier l'icône source pour référence
    const iconExt = path.extname(iconPath);
    const sourceCopy = path.join(__dirname, 'public', `icon-source${iconExt}`);
    fs.copyFileSync(iconPath, sourceCopy);
    console.log(`✓ Copie de l'icône source sauvegardée`);

    console.log('\n🎉 Toutes les icônes PWA ont été générées avec succès!');
    console.log('Vous pouvez maintenant builder votre application avec: npm run build');
  } catch (error) {
    console.error('❌ Erreur lors de la génération des icônes:', error.message);
    process.exit(1);
  }
}

findAndReplaceIcon();