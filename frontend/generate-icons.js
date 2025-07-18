const sharp = require('sharp');
const fs = require('fs');

async function generateIcons() {
  const svgBuffer = fs.readFileSync('./public/icon.svg');
  
  const sizes = [
    { size: 64, name: 'pwa-64x64.png' },
    { size: 192, name: 'pwa-192x192.png' },
    { size: 512, name: 'pwa-512x512.png' },
    { size: 512, name: 'maskable-icon-512x512.png' },
    { size: 180, name: 'apple-touch-icon.png' },
    { size: 32, name: 'favicon.ico' }
  ];

  for (const { size, name } of sizes) {
    await sharp(svgBuffer)
      .resize(size, size)
      .png()
      .toFile(`./public/${name}`);
    
    console.log(`Generated ${name}`);
  }
}

generateIcons().catch(console.error);