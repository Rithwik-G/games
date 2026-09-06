(() => {
  const colors = { ink: '#252521', red: '#c94e43', blue: '#496aaa', green: '#4f7b5d', orange: '#d9853d', violet: '#705b90', paper: '#eeece5' };
  const line = '#c5c2b9';
  document.querySelectorAll('[data-preview] canvas').forEach((canvas) => {
    const ctx = canvas.getContext('2d'); const type = canvas.closest('[data-preview]').dataset.preview;
    ctx.fillStyle = colors.paper; ctx.fillRect(0, 0, 600, 360); ctx.strokeStyle = line; ctx.lineWidth = 2;
    if (type === 'connect-four') {
      ctx.fillStyle = colors.blue; ctx.fillRect(86, 54, 428, 252);
      for (let y=0;y<6;y++) for (let x=0;x<7;x++) { ctx.beginPath(); ctx.arc(123+x*59, 82+y*39, 14, 0, Math.PI*2); ctx.fillStyle = [[3,5],[3,4],[2,5],[4,5]].some(([a,b])=>a===x&&b===y) ? colors.red : (x===4&&y===4 ? '#dab64c' : colors.paper); ctx.fill(); }
    } else if (type === 'snake') {
      ctx.fillStyle = colors.ink; ctx.fillRect(92, 34, 416, 292); ctx.strokeStyle='#343430'; ctx.lineWidth=1;
      for(let x=0;x<=20;x++){ctx.beginPath();ctx.moveTo(92+x*20.8,34);ctx.lineTo(92+x*20.8,326);ctx.stroke();}
      for(let y=0;y<=14;y++){ctx.beginPath();ctx.moveTo(92,34+y*20.8);ctx.lineTo(508,34+y*20.8);ctx.stroke();}
      ctx.fillStyle='#69a474'; [[8,7],[9,7],[10,7],[10,8],[10,9],[11,9],[12,9]].forEach(([x,y])=>ctx.fillRect(94+x*20.8,36+y*20.8,17,17)); ctx.fillStyle=colors.red; ctx.fillRect(94+15*20.8,36+5*20.8,17,17);
    } else if (type === 'hangman') {
      ctx.strokeStyle=colors.ink; ctx.lineWidth=5; ctx.lineCap='round'; [[170,280,350,280],[230,280,230,70],[230,70,355,70],[355,70,355,105]].forEach(p=>{ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(p[2],p[3]);ctx.stroke();}); ctx.beginPath();ctx.arc(355,130,25,0,Math.PI*2);ctx.stroke(); [[355,155,355,220],[355,170,320,196],[355,170,390,196]].forEach(p=>{ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(p[2],p[3]);ctx.stroke();}); for(let i=0;i<5;i++){ctx.beginPath();ctx.moveTo(160+i*70,320);ctx.lineTo(210+i*70,320);ctx.stroke();}
    } else if (type === 'rubiks-cube') {
      const fc=['#f3f1ea','#c94e43','#4f7b5d','#d5b94c','#d9853d','#496aaa']; let k=0; [[3,0],[0,3],[3,3],[6,3],[9,3],[3,6]].forEach(([ox,oy])=>{ctx.fillStyle=fc[k++];for(let y=0;y<3;y++)for(let x=0;x<3;x++)ctx.fillRect(96+(ox+x)*34,44+(oy+y)*34,30,30);});
    } else if (type === 'space-invaders') {
      ctx.fillStyle=colors.ink;ctx.fillRect(0,0,600,360);ctx.fillStyle='#d8d6ce'; for(let i=0;i<38;i++){const x=(i*137)%600,y=(i*71)%330;ctx.fillRect(x,y,2,2);} ctx.fillStyle='#899bca'; for(let i=0;i<6;i++){const x=90+i*75,y=70+(i%2)*34;ctx.fillRect(x,y,31,16);ctx.fillRect(x+6,y-6,19,27);} ctx.fillStyle='#dedbd2';ctx.fillRect(276,294,48,18);ctx.fillRect(288,280,24,22);ctx.fillStyle=colors.red;ctx.fillRect(299,220,3,45);
    } else if (type === 'tic-tac-toe') {
      ctx.strokeStyle=colors.ink;ctx.lineWidth=5;[250,350].forEach(x=>{ctx.beginPath();ctx.moveTo(x,35);ctx.lineTo(x,325);ctx.stroke();});[132,228].forEach(y=>{ctx.beginPath();ctx.moveTo(155,y);ctx.lineTo(445,y);ctx.stroke();}); ctx.font='68px system-ui';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=colors.red;ctx.fillText('×',202,83);ctx.fillText('×',400,277);ctx.fillStyle=colors.blue;ctx.fillText('○',301,180);ctx.fillText('○',202,277);
    } else if (type === 'sorting-lab') {
      const vals=[.2,.48,.32,.7,.57,.86,.4,.66,.28,.92,.52,.77,.62,.95];vals.forEach((v,i)=>{ctx.fillStyle=i===7?colors.red:colors.ink;ctx.fillRect(80+i*33,305-v*245,20,v*245);});
    } else {
      const size=18, ox=57,oy=36;for(let y=0;y<16;y++)for(let x=0;x<27;x++){ctx.fillStyle=((x*7+y*11)%13===0&&x>2&&x<24)?colors.ink:((x+y)>13&&(x+y)<32?'#c9d5c8':'#e4e2db');ctx.fillRect(ox+x*size,oy+y*size,size-1,size-1);}ctx.fillStyle=colors.red;ctx.fillRect(ox+2*size,oy+2*size,size-1,size-1);ctx.fillStyle=colors.blue;ctx.fillRect(ox+24*size,oy+13*size,size-1,size-1);
    }
  });
})();
