(() => {
  const root = document.getElementById('game-root');
  const status = document.getElementById('game-status');
  const restartButton = document.getElementById('global-restart');
  if (!root) return;
  let restart = () => location.reload();
  const setStatus = (message) => { status.textContent = message; };
  const button = (label, onClick, className = '') => {
    const el = document.createElement('button'); el.type = 'button'; el.textContent = label; el.className = className; el.addEventListener('click', onClick); return el;
  };
  restartButton.addEventListener('click', () => restart());

  function connectFour() {
    root.innerHTML = '<div class="game-stack"><p class="game-caption">You are yellow · the computer opens</p><div class="connect-board" role="grid" aria-label="Connect Four board"></div></div>';
    const boardEl = root.querySelector('.connect-board');
    let board, over, thinking;
    const cells = Array.from({ length: 42 }, (_, i) => {
      const el = document.createElement('button'); el.type = 'button'; el.className = 'connect-cell'; el.setAttribute('aria-label', `Row ${Math.floor(i/7)+1}, column ${i%7+1}`); el.addEventListener('click', () => humanMove(i % 7)); boardEl.append(el); return el;
    });
    const lines = () => {
      const all=[]; for(let r=0;r<6;r++)for(let c=0;c<7;c++)[[0,1],[1,0],[1,1],[1,-1]].forEach(([dr,dc])=>{const line=[];for(let k=0;k<4;k++){const y=r+dr*k,x=c+dc*k;if(y>=0&&y<6&&x>=0&&x<7)line.push(y*7+x);}if(line.length===4)all.push(line);}); return all;
    };
    const wins = lines();
    const winner = (b) => { for (const line of wins) { const p=b[line[0]]; if(p && line.every(i=>b[i]===p)) return [p,line]; } return b.every(Boolean) ? [3,[]] : null; };
    const drop = (b, col, player) => { for(let r=5;r>=0;r--){const i=r*7+col;if(!b[i]){b[i]=player;return i;}} return -1; };
    const scoreWindow = (values) => { const a=values.filter(v=>v===1).length,h=values.filter(v=>v===2).length,e=4-a-h; if(a===4)return 100000;if(h===4)return -100000;if(a===3&&e===1)return 80;if(a===2&&e===2)return 12;if(h===3&&e===1)return -95;if(h===2&&e===2)return -10;return 0; };
    const evaluate = (b) => wins.reduce((sum,line)=>sum+scoreWindow(line.map(i=>b[i])), b.filter((v,i)=>v===1&&i%7===3).length*8);
    const minimax = (b, depth, alpha, beta, max) => {
      const result=winner(b); if(result) return result[0]===1 ? 1000000+depth : result[0]===2 ? -1000000-depth : 0; if(depth===0)return evaluate(b);
      if(max){let value=-Infinity;for(const c of [3,2,4,1,5,0,6]){const copy=b.slice();if(drop(copy,c,1)<0)continue;value=Math.max(value,minimax(copy,depth-1,alpha,beta,false));alpha=Math.max(alpha,value);if(alpha>=beta)break;}return value;}
      let value=Infinity;for(const c of [3,2,4,1,5,0,6]){const copy=b.slice();if(drop(copy,c,2)<0)continue;value=Math.min(value,minimax(copy,depth-1,alpha,beta,true));beta=Math.min(beta,value);if(alpha>=beta)break;}return value;
    };
    const draw = (winning=[]) => cells.forEach((el,i)=>{el.className='connect-cell'+(board[i]===1?' red':board[i]===2?' yellow':'')+(winning.includes(i)?' win':'');el.disabled=over||thinking;});
    const finish = () => { const result=winner(board); if(!result)return false; over=true; draw(result[1]); setStatus(result[0]===1?'Computer wins':result[0]===2?'You win':'Draw'); return true; };
    const aiMove = () => { if(over)return;thinking=true;setStatus('Computer thinking');draw();setTimeout(()=>{let best=-Infinity,choices=[];for(const c of [3,2,4,1,5,0,6]){const copy=board.slice();if(drop(copy,c,1)<0)continue;const value=minimax(copy,5,-Infinity,Infinity,false);if(value>best){best=value;choices=[c];}else if(value===best)choices.push(c);}drop(board,choices[0],1);thinking=false;draw();if(!finish())setStatus('Your turn · yellow');},180); };
    const humanMove = (col) => { if(over||thinking||drop(board,col,2)<0)return;draw();if(!finish())aiMove(); };
    restart = () => { board=Array(42).fill(0);over=false;thinking=false;draw();aiMove(); };
    restart();
  }

  function snakeGame() {
    root.innerHTML = '<div class="game-stack"><div class="game-toolbar"></div><div class="canvas-wrap"><canvas class="game-canvas" width="600" height="600"></canvas><div class="game-overlay"><div class="overlay-card"><h2>Snake</h2><p>Fill the board without hitting a wall.</p><button class="primary-button" type="button">Start</button></div></div></div><div class="touch-controls" aria-label="Touch controls"><button data-dir="left">←</button><button data-dir="up">↑</button><button data-dir="down">↓</button><button data-dir="right">→</button></div></div>';
    const canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d'),overlay=root.querySelector('.game-overlay'),toolbar=root.querySelector('.game-toolbar');
    let snake, apple, dir, nextDir, timer, playing=false, paused=false, ai=false;
    const modePlay=button('Play yourself',()=>{ai=false;restart();start();},'primary-button'); const modeAI=button('Watch the AI',()=>{ai=true;restart();start();}); const pause=button('Pause',()=>togglePause()); toolbar.append(modePlay,modeAI,pause);
    const cycle=[[0,0]];for(let x=1;x<20;x++)cycle.push([x,0]);for(let x=19;x>=1;x--){if((19-x)%2===0){for(let y=1;y<20;y++)cycle.push([x,y]);}else{for(let y=19;y>=1;y--)cycle.push([x,y]);}}for(let y=19;y>=1;y--)cycle.push([0,y]);
    const key=(p)=>p.join(','); const cycleIndex=new Map(cycle.map((p,i)=>[key(p),i]));
    const placeApple=()=>{const free=[];for(let y=0;y<20;y++)for(let x=0;x<20;x++)if(!snake.some(p=>p[0]===x&&p[1]===y))free.push([x,y]);apple=free[Math.floor(Math.random()*free.length)]||null;};
    const draw=()=>{ctx.fillStyle='#171714';ctx.fillRect(0,0,600,600);ctx.strokeStyle='#252522';ctx.lineWidth=1;for(let i=0;i<=20;i++){ctx.beginPath();ctx.moveTo(i*30,0);ctx.lineTo(i*30,600);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i*30);ctx.lineTo(600,i*30);ctx.stroke();}snake.forEach((p,i)=>{ctx.fillStyle=i===0?'#8abc8c':'#5e956b';ctx.fillRect(p[0]*30+2,p[1]*30+2,26,26);});if(apple){ctx.fillStyle='#d9523e';ctx.fillRect(apple[0]*30+4,apple[1]*30+4,22,22);}ctx.fillStyle='#d7d4cc';ctx.font='18px ui-monospace';ctx.fillText(String(Math.max(0,snake.length-3)).padStart(2,'0'),16,28);};
    const setDirection=(d)=>{if(ai)return;const opp={up:'down',down:'up',left:'right',right:'left'};if(d!==opp[dir])nextDir=d;};
    const tick=()=>{if(!playing||paused)return;if(ai){const i=cycleIndex.get(key(snake[0]));const n=cycle[(i+1)%cycle.length];dir=n[0]>snake[0][0]?'right':n[0]<snake[0][0]?'left':n[1]>snake[0][1]?'down':'up';}else dir=nextDir; const delta={up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]}[dir];const head=[snake[0][0]+delta[0],snake[0][1]+delta[1]];const eating=apple&&head[0]===apple[0]&&head[1]===apple[1];const body=eating?snake:snake.slice(0,-1);if(head[0]<0||head[0]>=20||head[1]<0||head[1]>=20||body.some(p=>key(p)===key(head))){playing=false;overlay.hidden=false;overlay.querySelector('h2').textContent='Game over';overlay.querySelector('p').textContent=`Score ${Math.max(0,snake.length-3)}`;overlay.querySelector('button').textContent='Try again';setStatus('Game over');return;}snake.unshift(head);if(eating)placeApple();else snake.pop();draw();setStatus(`${ai?'AI running':'Playing'} · score ${snake.length-3}`);if(snake.length===400){playing=false;setStatus('Perfect board');}}
    const start=()=>{overlay.hidden=true;playing=true;paused=false;pause.textContent='Pause';clearInterval(timer);timer=setInterval(tick,100);setStatus(ai?'AI running':'Playing');};
    const togglePause=()=>{if(!playing)return;paused=!paused;pause.textContent=paused?'Resume':'Pause';setStatus(paused?'Paused':ai?'AI running':'Playing');};
    restart=()=>{clearInterval(timer);playing=false;paused=false;if(ai){snake=[cycle[0],cycle[cycle.length-1],cycle[cycle.length-2]];dir='right';}else{snake=[[10,10],[10,11],[10,12]];dir='up';}nextDir=dir;placeApple();draw();overlay.hidden=false;overlay.querySelector('h2').textContent=ai?'Snake AI':'Snake';overlay.querySelector('p').textContent=ai?'Following a Hamiltonian cycle.':'Fill the board without hitting a wall.';overlay.querySelector('button').textContent=ai?'Run AI':'Start';setStatus('Ready');modePlay.classList.toggle('primary-button',!ai);modeAI.classList.toggle('primary-button',ai);};
    overlay.querySelector('button').addEventListener('click',start);root.querySelectorAll('[data-dir]').forEach(b=>b.addEventListener('click',()=>setDirection(b.dataset.dir)));window.addEventListener('keydown',e=>{const map={ArrowUp:'up',w:'up',ArrowDown:'down',s:'down',ArrowLeft:'left',a:'left',ArrowRight:'right',d:'right'};if(map[e.key]){e.preventDefault();setDirection(map[e.key]);}if(e.code==='Space'){e.preventDefault();togglePause();}if(e.key.toLowerCase()==='r')restart();});restart();
  }

  function hangman() {
    let phrase='',guessed=new Set(),misses=0,ended=false;
    const setup=()=>{phrase='';root.innerHTML='<form class="secret-form"><p class="eyebrow">Player one</p><h2>Choose a secret phrase.</h2><p>It stays hidden after you hand over the screen.</p><label for="secret">Word or phrase</label><input id="secret" type="password" autocomplete="off" maxlength="36" pattern="[A-Za-z \'-]+" required><button class="primary-button">Hide phrase & begin</button></form>';setStatus('Waiting for a secret phrase');const form=root.querySelector('form');form.addEventListener('submit',e=>{e.preventDefault();phrase=form.querySelector('input').value.trim().toUpperCase();if(!/[A-Z]/.test(phrase))return;guessed=new Set();misses=0;ended=false;render();});setTimeout(()=>root.querySelector('input').focus(),0);};
    const render=()=>{root.innerHTML=`<div class="hangman-layout"><svg class="hangman-svg" viewBox="0 0 300 340" aria-label="Hangman drawing"><g fill="none" stroke="#171714" stroke-width="5" stroke-linecap="round"><path d="M30 315H250M70 315V30H205V62"/><circle class="hangman-part" cx="205" cy="88" r="26"/><path class="hangman-part" d="M205 114V205"/><path class="hangman-part" d="M205 140L163 172"/><path class="hangman-part" d="M205 140L247 172"/><path class="hangman-part" d="M205 205L167 259"/><path class="hangman-part" d="M205 205L243 259"/><circle class="hangman-part" cx="196" cy="82" r="2" fill="#171714"/><circle class="hangman-part" cx="214" cy="82" r="2" fill="#171714"/><path class="hangman-part" d="M195 101Q205 92 215 101"/></g></svg><div><div class="word-display"></div><div class="keyboard"></div></div></div>`;const slots=root.querySelector('.word-display');[...phrase].forEach(ch=>{const el=document.createElement('span');el.className='letter-slot'+(ch===' '?' space':'');el.textContent=ch===' '?'' : (!/[A-Z]/.test(ch)||guessed.has(ch)||ended?ch:'');slots.append(el);});root.querySelectorAll('.hangman-part').forEach((el,i)=>el.classList.toggle('visible',i<misses));const keyboard=root.querySelector('.keyboard');'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(ch=>{const el=button(ch,()=>guess(ch));el.disabled=guessed.has(ch)||ended;keyboard.append(el);});const letters=[...phrase].filter(c=>/[A-Z]/.test(c));const won=letters.every(c=>guessed.has(c));if(won&&!ended){ended=true;setStatus('Phrase solved');}else if(misses>=9&&!ended){ended=true;setStatus(`Out of guesses · ${phrase}`);}else if(!ended)setStatus(`${9-misses} wrong guesses left`);if(ended){setTimeout(()=>{const again=button('New phrase',setup,'primary-button');keyboard.replaceChildren(again);},0);}};
    const guess=(ch)=>{if(ended||guessed.has(ch))return;guessed.add(ch);if(!phrase.includes(ch))misses++;render();};restart=setup;window.addEventListener('keydown',e=>{const ch=e.key.toUpperCase();if(/^[A-Z]$/.test(ch)&&phrase)guess(ch);if(e.key.toLowerCase()==='r'&&phrase)setup();});setup();
  }

  function rubiksCube() {
    root.innerHTML='<div class="cube-workbench"><div class="cube-net" aria-label="Rubik’s cube net"></div><div class="cube-moves"></div><p class="move-log"></p><div class="game-toolbar cube-actions"></div></div>';
    const net=root.querySelector('.cube-net'),movesEl=root.querySelector('.cube-moves'),log=root.querySelector('.move-log'),actions=root.querySelector('.cube-actions');
    let stickers=[],history=[],solving=false;
    const colors={U:'#f3f1ea',D:'#e1bf49',F:'#4f855e',B:'#4b68ad',R:'#c94e43',L:'#dc873c'};
    const add = (face, normal, positionFor) => {
      for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
          const position = positionFor(row, col);
          stickers.push({ p: [...position], n: [...normal], color: colors[face] });
        }
      }
    };
    const resetState=()=>{stickers=[];add('U',[0,1,0],(r,c)=>[c-1,1,r-1]);add('D',[0,-1,0],(r,c)=>[c-1,-1,1-r]);add('F',[0,0,1],(r,c)=>[c-1,1-r,1]);add('B',[0,0,-1],(r,c)=>[1-c,1-r,-1]);add('R',[1,0,0],(r,c)=>[1,1-r,1-c]);add('L',[-1,0,0],(r,c)=>[-1,1-r,c-1]);history=[];solving=false;render();setStatus('Solved');};
    const faceOf=n=>n[1]===1?'U':n[1]===-1?'D':n[2]===1?'F':n[2]===-1?'B':n[0]===1?'R':'L';
    const rc=(face,p)=>({U:[p[2]+1,p[0]+1],D:[1-p[2],p[0]+1],F:[1-p[1],p[0]+1],B:[1-p[1],1-p[0]],R:[1-p[1],1-p[2]],L:[1-p[1],p[2]+1]}[face]);
    const offset={U:[0,3],L:[3,0],F:[3,3],R:[3,6],B:[3,9],D:[6,3]};
    const render=()=>{net.replaceChildren();stickers.forEach(s=>{const face=faceOf(s.n),[r,c]=rc(face,s.p),[or,oc]=offset[face];const el=document.createElement('div');el.className='sticker';el.style.background=s.color;el.style.gridRow=or+r+1;el.style.gridColumn=oc+c+1;net.append(el);});log.textContent=history.length?history.slice(-24).join('  '):'No moves yet';};
    const rotateVec=(v,axis,d)=>{let [x,y,z]=v;if(axis==='x')return [x,d>0?-z:z,d>0?y:-y];if(axis==='y')return [d>0?z:-z,y,d>0?-x:x];return [d>0?-y:y,d>0?x:-x,z];};
    const base={R:['x',1,-1],L:['x',-1,1],U:['y',1,1],D:['y',-1,-1],F:['z',1,-1],B:['z',-1,1]};
    const turn=(move,record=true)=>{const face=move[0],[axis,layer,normalDir]=base[face];const d=move.includes("'")?-normalDir:normalDir;stickers.forEach(s=>{if(s.p['xyz'.indexOf(axis)]===layer){s.p=rotateVec(s.p,axis,d);s.n=rotateVec(s.n,axis,d);}});if(record)history.push(move);render();setStatus(history.length?`${history.length} move${history.length===1?'':'s'}`:'Solved');};
    'R L U D F B'.split(' ').forEach(face=>{const el=button(face,e=>{if(!solving)turn(e.shiftKey?face+"'":face);});el.title=`${face}; Shift-click for ${face}′`;movesEl.append(el);});
    const scramble=()=>{if(solving)return;resetState();const faces='RLUDFB';let last='';for(let i=0;i<20;i++){let f;do{f=faces[Math.floor(Math.random()*6)];}while(f===last);last=f;turn(f+(Math.random()>.5?"'":''));}setStatus('Scrambled · 20 moves');};
    const solve=()=>{if(solving||!history.length)return;solving=true;const solution=history.slice().reverse().map(m=>m.includes("'")?m[0]:m+"'");history=[];let i=0;setStatus('Solving');const step=()=>{if(i>=solution.length){solving=false;render();setStatus('Solved');return;}turn(solution[i++],false);setStatus(`Solving · ${solution.length-i} moves left`);setTimeout(step,100);};step();};
    actions.append(button('Scramble',scramble,'primary-button'),button('Solve',solve),button('Reset',resetState));restart=resetState;window.addEventListener('keydown',e=>{const f=e.key.toUpperCase();if(base[f]&&!solving)turn(f+(e.shiftKey?"'":''));});resetState();
  }

  function spaceInvaders() {
    root.innerHTML='<div class="game-stack"><div class="canvas-wrap"><canvas class="game-canvas" width="800" height="600"></canvas><div class="game-overlay"><div class="overlay-card"><h2>Space Invaders</h2><p>Move, aim, and keep them above the line.</p><button class="primary-button">Start</button></div></div></div><div class="touch-controls"><button data-key="left">←</button><button data-key="fire">↑</button><button data-key="right">→</button></div></div>';
    const canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d'),overlay=root.querySelector('.game-overlay');let player,enemies,bullet,score,running=false,paused=false,last=0,keys={};const stars=Array.from({length:70},(_,i)=>[(i*137)%800,(i*83)%600,1+(i%3===0)]);
    const reset=()=>{player={x:370,y:520};enemies=Array.from({length:6},(_,i)=>({x:45+i*122,y:70+(i%2)*55,dx:95}));bullet=null;score=0;running=false;paused=false;overlay.hidden=false;overlay.querySelector('h2').textContent='Space Invaders';overlay.querySelector('p').textContent='Move, aim, and keep them above the line.';overlay.querySelector('button').textContent='Start';setStatus('Ready');draw();};
    const fire=()=>{if(running&&!paused&&!bullet)bullet={x:player.x+30,y:player.y-10};};
    const drawAlien=(x,y)=>{ctx.fillStyle='#8da0ce';ctx.fillRect(x+8,y,32,8);ctx.fillRect(x,y+8,48,19);ctx.fillRect(x+5,y+27,10,8);ctx.fillRect(x+33,y+27,10,8);ctx.fillStyle='#171714';ctx.fillRect(x+11,y+13,6,6);ctx.fillRect(x+31,y+13,6,6);};
    const draw=()=>{ctx.fillStyle='#15151a';ctx.fillRect(0,0,800,600);ctx.fillStyle='#bbbcc2';stars.forEach(s=>ctx.fillRect(s[0],s[1],s[2],s[2]));ctx.strokeStyle='#3d3c43';ctx.setLineDash([5,8]);ctx.beginPath();ctx.moveTo(0,500);ctx.lineTo(800,500);ctx.stroke();ctx.setLineDash([]);enemies.forEach(e=>drawAlien(e.x,e.y));ctx.fillStyle='#e7e4da';ctx.fillRect(player.x,player.y+20,64,20);ctx.fillRect(player.x+20,player.y,24,25);if(bullet){ctx.fillStyle='#d9523e';ctx.fillRect(bullet.x,bullet.y,4,20);}ctx.fillStyle='#eeeae0';ctx.font='20px ui-monospace';ctx.fillText(`SCORE ${String(score).padStart(3,'0')}`,18,32);};
    const end=()=>{running=false;overlay.hidden=false;overlay.querySelector('h2').textContent='Game over';overlay.querySelector('p').textContent=`Score ${score}`;overlay.querySelector('button').textContent='Play again';setStatus('Game over');};
    const frame=(time)=>{const dt=Math.min(.035,(time-last)/1000||0);last=time;if(running&&!paused){if(keys.left)player.x-=260*dt;if(keys.right)player.x+=260*dt;player.x=Math.max(0,Math.min(736,player.x));let bounced=false;enemies.forEach(e=>{e.x+=e.dx*dt;if(e.x<=0||e.x>=752)bounced=true;});if(bounced)enemies.forEach(e=>{e.dx*=-1;e.x=Math.max(0,Math.min(752,e.x));e.y+=25;});if(bullet){bullet.y-=440*dt;if(bullet.y<0)bullet=null;else{const hit=enemies.findIndex(e=>Math.hypot((e.x+24)-bullet.x,(e.y+16)-bullet.y)<32);if(hit>=0){score++;const e=enemies[hit];e.x=20+Math.random()*710;e.y=55+Math.random()*90;bullet=null;setStatus(`Playing · score ${score}`);}}}if(enemies.some(e=>e.y>465))end();}draw();requestAnimationFrame(frame);};
    const start=()=>{reset();running=true;overlay.hidden=true;last=performance.now();setStatus('Playing');};restart=reset;overlay.querySelector('button').addEventListener('click',start);window.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Space'].includes(e.code))e.preventDefault();if(e.code==='ArrowLeft'||e.key==='a')keys.left=true;if(e.code==='ArrowRight'||e.key==='d')keys.right=true;if(e.code==='Space')fire();if(e.key.toLowerCase()==='p'&&running){paused=!paused;setStatus(paused?'Paused':'Playing');}if(e.key.toLowerCase()==='r')reset();});window.addEventListener('keyup',e=>{if(e.code==='ArrowLeft'||e.key==='a')keys.left=false;if(e.code==='ArrowRight'||e.key==='d')keys.right=false;});root.querySelectorAll('[data-key]').forEach(el=>{const k=el.dataset.key;if(k==='fire')el.addEventListener('click',fire);else{el.addEventListener('pointerdown',()=>keys[k]=true);el.addEventListener('pointerup',()=>keys[k]=false);el.addEventListener('pointerleave',()=>keys[k]=false);}});reset();requestAnimationFrame(frame);
  }

  function ticTacToe() {
    root.innerHTML='<div class="game-stack"><p class="game-caption">You are O · the computer is X</p><div class="ttt-board" role="grid"></div></div>';const boardEl=root.querySelector('.ttt-board');let board,over,thinking;const cells=Array.from({length:9},(_,i)=>{const el=button('',()=>human(i));el.className='ttt-cell';el.setAttribute('aria-label',`Square ${i+1}`);boardEl.append(el);return el;});const winLines=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];const result=b=>{for(const l of winLines)if(b[l[0]]&&l.every(i=>b[i]===b[l[0]]))return [b[l[0]],l];return b.every(Boolean)?['draw',[]]:null;};const minimax=(b,max,depth=0)=>{const r=result(b);if(r)return r[0]==='X'?10-depth:r[0]==='O'?depth-10:0;let best=max?-Infinity:Infinity;for(let i=0;i<9;i++)if(!b[i]){b[i]=max?'X':'O';const s=minimax(b,!max,depth+1);b[i]='';best=max?Math.max(best,s):Math.min(best,s);}return best;};const draw=(line=[])=>cells.forEach((el,i)=>{el.textContent=board[i]==='X'?'×':board[i]==='O'?'○':'';el.disabled=over||thinking||!!board[i];el.classList.toggle('win',line.includes(i));});const finish=()=>{const r=result(board);if(!r)return false;over=true;draw(r[1]);setStatus(r[0]==='draw'?'Draw':r[0]==='O'?'You win':'Computer wins');return true;};const ai=()=>{thinking=true;draw();setStatus('Computer thinking');setTimeout(()=>{let best=-Infinity,move=-1;for(let i=0;i<9;i++)if(!board[i]){board[i]='X';const s=minimax(board,false);board[i]='';if(s>best){best=s;move=i;}}board[move]='X';thinking=false;draw();if(!finish())setStatus('Your turn · O');},220);};const human=i=>{if(over||thinking||board[i])return;board[i]='O';draw();if(!finish())ai();};restart=()=>{board=Array(9).fill('');over=false;thinking=false;draw();ai();};restart();
  }

  function sortingLab() {
    root.innerHTML='<div class="lab-shell"><div class="lab-toolbar"><select aria-label="Sorting algorithm"><option value="quick">Quick sort</option><option value="merge">Merge sort</option><option value="insertion">Insertion sort</option><option value="selection">Selection sort</option><option value="bubble">Bubble sort</option></select><button class="primary-button run">Run</button><button class="shuffle">New array</button><button class="pause">Pause</button><span class="spacer"></span><span class="lab-stat"></span></div><canvas class="lab-canvas" width="900" height="500"></canvas></div>';
    const canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d'),select=root.querySelector('select'),runButton=root.querySelector('.run'),pauseButton=root.querySelector('.pause'),stat=root.querySelector('.lab-stat');let values,ops,index,running=false,paused=false,timer,active=[];
    const fresh=()=>{clearTimeout(timer);values=Array.from({length:60},(_,i)=>i+1);for(let i=values.length-1;i;i--){const j=Math.floor(Math.random()*(i+1));[values[i],values[j]]=[values[j],values[i]];}ops=[];index=0;running=false;paused=false;active=[];pauseButton.textContent='Pause';draw();setStatus('Ready');};
    const draw=()=>{ctx.fillStyle='#eeece5';ctx.fillRect(0,0,900,500);const w=900/values.length;values.forEach((v,i)=>{ctx.fillStyle=active.includes(i)?'#d9523e':'#252521';ctx.fillRect(i*w+1,480-v*7.3,w-2,v*7.3);});stat.textContent=`${index} operations`;};
    const operations=(input,type)=>{const a=input.slice(),out=[];const swap=(i,j)=>{out.push(['compare',i,j]);[a[i],a[j]]=[a[j],a[i]];out.push(['swap',i,j]);};if(type==='bubble'){for(let end=a.length-1;end>0;end--)for(let i=0;i<end;i++){out.push(['compare',i,i+1]);if(a[i]>a[i+1])swap(i,i+1);}}else if(type==='selection'){for(let i=0;i<a.length-1;i++){let m=i;for(let j=i+1;j<a.length;j++){out.push(['compare',m,j]);if(a[j]<a[m])m=j;}if(m!==i)swap(i,m);}}else if(type==='insertion'){for(let i=1;i<a.length;i++){let j=i;while(j>0){out.push(['compare',j-1,j]);if(a[j-1]<=a[j])break;swap(j-1,j);j--;}}}else if(type==='merge'){const sort=(lo,hi)=>{if(hi-lo<2)return;const mid=(lo+hi)>>1;sort(lo,mid);sort(mid,hi);const merged=[],left=a.slice(lo,mid),right=a.slice(mid,hi);let l=0,r=0;while(l<left.length||r<right.length){out.push(['compare',lo+l,mid+r]);merged.push(r>=right.length||(l<left.length&&left[l]<=right[r])?left[l++]:right[r++]);}merged.forEach((v,i)=>{a[lo+i]=v;out.push(['set',lo+i,v]);});};sort(0,a.length);}else{const sort=(lo,hi)=>{if(lo>=hi)return;const pivot=a[hi];let p=lo;for(let j=lo;j<hi;j++){out.push(['compare',j,hi]);if(a[j]<pivot){if(p!==j)swap(p,j);p++;}}swap(p,hi);sort(lo,p-1);sort(p+1,hi);};sort(0,a.length-1);}return out;};
    const step=()=>{if(!running||paused)return;if(index>=ops.length){running=false;active=[];draw();setStatus(`Sorted · ${index} operations`);return;}const op=ops[index++];active=op.slice(1,3).filter(Number.isInteger);if(op[0]==='swap')[values[op[1]],values[op[2]]]=[values[op[2]],values[op[1]]];else if(op[0]==='set')values[op[1]]=op[2];draw();timer=setTimeout(step,select.value==='bubble'?2:8);};
    const run=()=>{if(running)return;ops=operations(values,select.value);index=0;running=true;paused=false;setStatus(`Running ${select.options[select.selectedIndex].text}`);step();};runButton.addEventListener('click',run);root.querySelector('.shuffle').addEventListener('click',fresh);pauseButton.addEventListener('click',()=>{if(!running)return;paused=!paused;pauseButton.textContent=paused?'Resume':'Pause';setStatus(paused?'Paused':`Running ${select.options[select.selectedIndex].text}`);if(!paused)step();});restart=fresh;fresh();
  }

  function pathfindingLab() {
    root.innerHTML='<div class="lab-shell"><div class="lab-toolbar"><select aria-label="Pathfinding algorithm"><option value="astar">A* · Manhattan</option><option value="dijkstra">Dijkstra</option><option value="bfs">Breadth-first</option><option value="dfs">Depth-first</option><option value="greedy">Greedy best-first</option></select><button class="primary-button visualize">Visualize</button><button class="maze">Make maze</button><button class="clear">Clear</button><span class="spacer"></span><span class="lab-stat"></span></div><canvas class="lab-canvas" width="775" height="475"></canvas><p class="game-caption">Red is the start. Blue is the target. Drag across the grid to add or erase walls.</p></div>';
    const canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d'),select=root.querySelector('select'),stat=root.querySelector('.lab-stat');const cols=31,rows=19,size=25,start=[1,1],goal=[29,17];let walls=new Set(),visited=new Set(),path=new Set(),drawing=false,erase=false,timer;
    const k=p=>p.join(',');const draw=()=>{ctx.fillStyle='#eeece5';ctx.fillRect(0,0,canvas.width,canvas.height);for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){const id=`${x},${y}`;ctx.fillStyle=walls.has(id)?'#272722':path.has(id)?'#d6b84b':visited.has(id)?'#c9d7c8':'#eeece5';ctx.fillRect(x*size,y*size,size-1,size-1);}ctx.fillStyle='#d9523e';ctx.fillRect(start[0]*size,start[1]*size,size-1,size-1);ctx.fillStyle='#496aaa';ctx.fillRect(goal[0]*size,goal[1]*size,size-1,size-1);};
    const clearSearch=()=>{clearInterval(timer);visited.clear();path.clear();};const neighbors=([x,y])=>[[x+1,y],[x-1,y],[x,y+1],[x,y-1]].filter(([a,b])=>a>=0&&a<cols&&b>=0&&b<rows&&!walls.has(`${a},${b}`));const heuristic=p=>Math.abs(goal[0]-p[0])+Math.abs(goal[1]-p[1]);
    const search=type=>{const frontier=[start],seen=new Set([k(start)]),came=new Map(),cost=new Map([[k(start),0]]),order=[];let found=false;while(frontier.length){let current;if(type==='dfs')current=frontier.pop();else if(type==='bfs')current=frontier.shift();else{frontier.sort((a,b)=>{const ca=cost.get(k(a)),cb=cost.get(k(b));const fa=type==='greedy'?heuristic(a):type==='astar'?ca+heuristic(a):ca;const fb=type==='greedy'?heuristic(b):type==='astar'?cb+heuristic(b):cb;return fa-fb;});current=frontier.shift();}order.push(current);if(k(current)===k(goal)){found=true;break;}for(const n of neighbors(current)){const id=k(n),nc=(cost.get(k(current))||0)+1;if(!seen.has(id)||nc<(cost.get(id)||Infinity)){seen.add(id);came.set(id,current);cost.set(id,nc);frontier.push(n);}}}const route=[];if(found){let cur=goal;while(k(cur)!==k(start)){route.push(cur);cur=came.get(k(cur));}route.reverse();}return {order,route};};
    const visualize=()=>{clearSearch();const result=search(select.value);let i=0;setStatus(`Running ${select.options[select.selectedIndex].text}`);timer=setInterval(()=>{for(let n=0;n<3&&i<result.order.length;n++,i++)visited.add(k(result.order[i]));stat.textContent=`${Math.min(i,result.order.length)} cells visited`;draw();if(i>=result.order.length){clearInterval(timer);let j=0;timer=setInterval(()=>{if(j>=result.route.length){clearInterval(timer);setStatus(result.route.length?`Path found · ${result.route.length} steps`:'No path found');return;}path.add(k(result.route[j++]));draw();},18);}},12);};
    const makeMaze=()=>{clearSearch();walls=new Set();for(let y=0;y<rows;y++)for(let x=0;x<cols;x++)walls.add(`${x},${y}`);const stack=[[1,1]],seen=new Set(['1,1']);walls.delete('1,1');while(stack.length){const cur=stack[stack.length-1];const opts=[[2,0],[-2,0],[0,2],[0,-2]].map(([dx,dy])=>[cur[0]+dx,cur[1]+dy,dx,dy]).filter(([x,y])=>x>0&&x<cols-1&&y>0&&y<rows-1&&!seen.has(`${x},${y}`));if(!opts.length){stack.pop();continue;}const [x,y,dx,dy]=opts[Math.floor(Math.random()*opts.length)];seen.add(`${x},${y}`);walls.delete(`${cur[0]+dx/2},${cur[1]+dy/2}`);walls.delete(`${x},${y}`);stack.push([x,y]);}walls.delete(k(goal));draw();setStatus('Maze ready');};
    const pointerCell=e=>{const r=canvas.getBoundingClientRect();return [Math.floor((e.clientX-r.left)*canvas.width/r.width/size),Math.floor((e.clientY-r.top)*canvas.height/r.height/size)];};const edit=e=>{const p=pointerCell(e),id=k(p);if(id===k(start)||id===k(goal))return;if(erase)walls.delete(id);else walls.add(id);draw();};canvas.addEventListener('pointerdown',e=>{e.preventDefault();clearSearch();drawing=true;const id=k(pointerCell(e));erase=walls.has(id);canvas.setPointerCapture(e.pointerId);edit(e);});canvas.addEventListener('pointermove',e=>{if(drawing)edit(e);});canvas.addEventListener('pointerup',()=>drawing=false);root.querySelector('.visualize').addEventListener('click',visualize);root.querySelector('.maze').addEventListener('click',makeMaze);root.querySelector('.clear').addEventListener('click',()=>{clearSearch();walls.clear();draw();setStatus('Board cleared');stat.textContent='';});restart=()=>{clearSearch();walls.clear();draw();setStatus('Ready');stat.textContent='';};restart();
  }

  function rubiksCube3D() {
    root.innerHTML = '<div class="cube-workbench"><div class="canvas-wrap cube-view"><canvas class="cube-canvas" width="720" height="540" aria-label="Interactive 3D Rubik’s Cube"></canvas><span class="drag-hint">Drag to rotate view</span></div><div class="cube-moves"></div><p class="move-log"></p><div class="game-toolbar cube-actions"></div><p class="game-caption">Interactive 3D cube · Python solver</p></div>';
    const canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d'),movesEl=root.querySelector('.cube-moves'),log=root.querySelector('.move-log'),actions=root.querySelector('.cube-actions');
    let stickers=[],history=[],solving=false,yaw=-.62,pitch=.46,dragging=false,lastPointer=null;
    const colors={U:'#f3f1ea',D:'#e1bf49',F:'#4f855e',B:'#4b68ad',R:'#c94e43',L:'#dc873c'};
    const add=(face,normal,positionFor)=>{for(let row=0;row<3;row++)for(let col=0;col<3;col++){const position=positionFor(row,col);stickers.push({p:[...position],n:[...normal],color:colors[face]});}};
    const resetState=()=>{stickers=[];add('U',[0,1,0],(r,c)=>[c-1,1,r-1]);add('D',[0,-1,0],(r,c)=>[c-1,-1,1-r]);add('F',[0,0,1],(r,c)=>[c-1,1-r,1]);add('B',[0,0,-1],(r,c)=>[1-c,1-r,-1]);add('R',[1,0,0],(r,c)=>[1,1-r,1-c]);add('L',[-1,0,0],(r,c)=>[-1,1-r,c-1]);history=[];solving=false;render();setStatus('Solved · Python model ready');};
    const rotateVec=(v,axis,d)=>{const[x,y,z]=v;if(axis==='x')return[x,d>0?-z:z,d>0?y:-y];if(axis==='y')return[d>0?z:-z,y,d>0?-x:x];return[d>0?-y:y,d>0?x:-x,z];};
    const moveMap={R:['x',1,-1],L:['x',-1,1],U:['y',1,-1],D:['y',-1,1],F:['z',1,-1],B:['z',-1,1]};
    const turn=(move,record=true)=>{const face=move[0],[axis,layer,clockwise]=moveMap[face],direction=move.includes("'")?-clockwise:clockwise;stickers.forEach(sticker=>{if(sticker.p['xyz'.indexOf(axis)]===layer){sticker.p=rotateVec(sticker.p,axis,direction);sticker.n=rotateVec(sticker.n,axis,direction);}});if(record)history.push(move);render();if(record)setStatus(`${history.length} move${history.length===1?'':'s'} · Python solver available`);};
    const cameraVector=point=>{let[x,y,z]=point;const cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);[x,z]=[x*cy+z*sy,-x*sy+z*cy];[y,z]=[y*cp-z*sp,y*sp+z*cp];return{x,y,z};};
    const camera=point=>{const{x,y,z}=cameraVector(point);const scale=95*6.5/(6.5-z);return{x:360+x*scale,y:270-y*scale,z};};
    const polygonFor=sticker=>{const n=sticker.n;let a,b;if(Math.abs(n[0])===1){a=[0,.43,0];b=[0,0,.43];}else if(Math.abs(n[1])===1){a=[.43,0,0];b=[0,0,.43];}else{a=[.43,0,0];b=[0,.43,0];}const center=sticker.p.map((v,i)=>v*1.02+n[i]*.53);return[[-1,-1],[1,-1],[1,1],[-1,1]].map(([u,v])=>camera(center.map((q,i)=>q+a[i]*u+b[i]*v)));};
    const render=()=>{ctx.fillStyle='#171714';ctx.fillRect(0,0,720,540);const faces=stickers.filter(sticker=>cameraVector(sticker.n).z>.02).map(sticker=>({sticker,points:polygonFor(sticker)}));faces.sort((a,b)=>a.points.reduce((n,p)=>n+p.z,0)-b.points.reduce((n,p)=>n+p.z,0));faces.forEach(({sticker,points})=>{ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.closePath();ctx.fillStyle=sticker.color;ctx.fill();ctx.strokeStyle='#171714';ctx.lineWidth=4;ctx.stroke();});log.textContent=history.length?history.slice(-28).join('  '):'No moves yet';};
    'R L U D F B'.split(' ').forEach(face=>{const el=button(face,event=>{if(!solving)turn(event.shiftKey?face+"'":face);});el.title=`${face}; Shift-click for ${face}′`;movesEl.append(el);});
    const scramble=()=>{if(solving)return;resetState();const faces='RLUDFB';let last='';for(let i=0;i<20;i++){let face;do{face=faces[Math.floor(Math.random()*6)];}while(face===last);last=face;turn(face+(Math.random()>.5?"'":''));}setStatus('Scrambled · Python solver ready');};
    const solve=async()=>{if(solving||!history.length)return;solving=true;actions.querySelectorAll('button').forEach(el=>el.disabled=true);setStatus('Running Python solver');try{const response=await fetch('/api/rubiks-cube/solve',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({moves:history})});if(!response.ok)throw new Error();const data=await response.json();history=[];let index=0;const step=()=>{if(index>=data.solution.length){solving=false;actions.querySelectorAll('button').forEach(el=>el.disabled=false);render();setStatus('Solved');return;}turn(data.solution[index++],false);setStatus(`Solving in Python · ${data.solution.length-index} moves left`);setTimeout(step,38);};step();}catch{solving=false;actions.querySelectorAll('button').forEach(el=>el.disabled=false);setStatus('Python solver could not complete');}};
    actions.append(button('Scramble',scramble,'primary-button'),button('Solve with Python',solve),button('Reset',resetState));
    canvas.addEventListener('pointerdown',event=>{dragging=true;lastPointer=[event.clientX,event.clientY];canvas.setPointerCapture(event.pointerId);});canvas.addEventListener('pointermove',event=>{if(!dragging)return;yaw+=(event.clientX-lastPointer[0])*.009;pitch=Math.max(-1.2,Math.min(1.2,pitch+(event.clientY-lastPointer[1])*.009));lastPointer=[event.clientX,event.clientY];render();});canvas.addEventListener('pointerup',()=>dragging=false);
    restart=resetState;window.addEventListener('keydown',event=>{const face=event.key.toUpperCase();if(moveMap[face]&&!solving)turn(face+(event.shiftKey?"'":''));});resetState();
  }

  function connectFourPython() {
    root.innerHTML = '<div class="game-stack"><p class="game-caption">Python engine · alpha-beta minimax</p><div class="connect-board" role="grid" aria-label="Connect Four board"></div></div>';
    const boardEl = root.querySelector('.connect-board');
    let state = null;
    let waiting = true;
    const cells = Array.from({length: 42}, (_, index) => {
      const cell = document.createElement('button');
      cell.type = 'button';
      cell.className = 'connect-cell';
      cell.setAttribute('aria-label', `Row ${Math.floor(index / 7) + 1}, column ${index % 7 + 1}`);
      cell.addEventListener('click', () => move(index % 7));
      boardEl.append(cell);
      return cell;
    });
    const winningLine = board => {
      for (let row=0; row<6; row++) for (let col=0; col<7; col++) {
        for (const [dy,dx] of [[0,1],[1,0],[1,1],[1,-1]]) {
          const line = Array.from({length:4},(_,i)=>(row+dy*i)*7+col+dx*i);
          if (line.every(i => i>=0 && i<42 && Math.floor(i/7)===row+dy*line.indexOf(i)) && board[line[0]] && line.every(i=>board[i]===board[line[0]])) return line;
        }
      }
      return [];
    };
    const render = () => {
      const flat = state ? state.board.flat() : Array(42).fill(0);
      const win = state?.winner ? winningLine(flat) : [];
      cells.forEach((cell,index) => {
        cell.className = 'connect-cell' + (flat[index]===1?' red':flat[index]===2?' yellow':'') + (win.includes(index)?' win':'');
        cell.disabled = waiting || Boolean(state?.winner);
      });
    };
    const announce = () => setStatus(state.winner===1?'Computer wins':state.winner===2?'You win':state.winner===3?'Draw':'Your turn · yellow · Python engine');
    const requestState = async (url, body) => {
      const response = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:body?JSON.stringify(body):undefined});
      if (!response.ok) throw new Error('Python game engine did not respond');
      return response.json();
    };
    const move = async column => {
      if (waiting || state?.winner) return;
      waiting = true; render(); setStatus('Minimax is thinking');
      try { state = await requestState('/api/connect-four/move', {column}); announce(); }
      catch (error) { setStatus('Could not reach Python engine'); }
      waiting = false; render();
    };
    restart = async () => {
      waiting = true; render(); setStatus('Starting Python engine');
      try { state = await requestState('/api/connect-four/new'); announce(); }
      catch (error) { setStatus('Could not reach Python engine'); }
      waiting = false; render();
    };
    restart();
  }

  function ticTacToePython() {
    root.innerHTML = '<div class="game-stack"><p class="game-caption">Python engine · alpha-beta minimax</p><div class="ttt-board" role="grid"></div></div>';
    const boardEl = root.querySelector('.ttt-board');
    let state = null;
    let waiting = true;
    const lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    const cells = Array.from({length:9},(_,index)=>{const cell=button('',()=>move(index));cell.className='ttt-cell';cell.setAttribute('aria-label',`Square ${index+1}`);boardEl.append(cell);return cell;});
    const render = () => {
      const flat = state ? state.board.flat() : Array(9).fill('N');
      const win = lines.find(line => flat[line[0]]!=='N' && line.every(i=>flat[i]===flat[line[0]])) || [];
      cells.forEach((cell,index)=>{cell.textContent=flat[index]==='X'?'×':flat[index]==='O'?'○':'';cell.disabled=waiting||flat[index]!=='N'||Boolean(state?.winner);cell.classList.toggle('win',win.includes(index));});
    };
    const announce = () => setStatus(state.winner==='X'?'Computer wins':state.winner==='O'?'You win':state.winner==='draw'?'Draw':'Your turn · O · Python engine');
    const requestState = async (url,body) => {const response=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined});if(!response.ok)throw new Error();return response.json();};
    const move = async index => {if(waiting||state?.winner)return;waiting=true;render();setStatus('Minimax is thinking');try{state=await requestState('/api/tic-tac-toe/move',{index});announce();}catch{setStatus('Could not reach Python engine');}waiting=false;render();};
    restart = async () => {waiting=true;render();setStatus('Starting Python engine');try{state=await requestState('/api/tic-tac-toe/new');announce();}catch{setStatus('Could not reach Python engine');}waiting=false;render();};
    restart();
  }

  function snakeGamePython() {
    root.innerHTML = '<div class="game-stack"><div class="game-toolbar"></div><div class="canvas-wrap"><canvas class="game-canvas" width="600" height="600"></canvas><div class="game-overlay"><div class="overlay-card"><h2>Snake</h2><p>Play on a 20 × 20 grid.</p><button class="primary-button" type="button">Start</button></div></div></div><div class="touch-controls" aria-label="Touch controls"><button data-dir="left">←</button><button data-dir="up">↑</button><button data-dir="down">↓</button><button data-dir="right">→</button></div><p class="game-caption">Python engine · movement and Hamiltonian shortcut logic</p></div>';
    const canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d'),overlay=root.querySelector('.game-overlay'),toolbar=root.querySelector('.game-toolbar');
    let state=null,playing=false,paused=false,ai=false,pendingDirection=null,timer=null,generation=0;
    const modePlay=button('Play yourself',()=>changeMode(false),'primary-button');
    const modeAI=button('Watch the AI',()=>changeMode(true));
    const pause=button('Pause',()=>togglePause());
    toolbar.append(modePlay,modeAI,pause);
    const requestState=async(url,body)=>{const response=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body||{})});if(!response.ok)throw new Error();return response.json();};
    const draw=()=>{ctx.fillStyle='#171714';ctx.fillRect(0,0,600,600);ctx.strokeStyle='#252522';ctx.lineWidth=1;for(let i=0;i<=20;i++){ctx.beginPath();ctx.moveTo(i*30,0);ctx.lineTo(i*30,600);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i*30);ctx.lineTo(600,i*30);ctx.stroke();}if(!state)return;state.snake.forEach((position,index)=>{ctx.fillStyle=index===0?'#8abc8c':'#5e956b';ctx.fillRect(position[0]*30+2,position[1]*30+2,26,26);});if(state.apple){ctx.fillStyle='#d9523e';ctx.fillRect(state.apple[0]*30+4,state.apple[1]*30+4,22,22);}ctx.fillStyle='#d7d4cc';ctx.font='18px ui-monospace';ctx.fillText(String(state.score).padStart(2,'0'),16,28);};
    const showOverlay=(title,copy,label)=>{overlay.hidden=false;overlay.querySelector('h2').textContent=title;overlay.querySelector('p').textContent=copy;overlay.querySelector('button').textContent=label;};
    const schedule=token=>{clearTimeout(timer);if(playing&&!paused)timer=setTimeout(()=>tick(token),ai?24:100);};
    const tick=async token=>{if(token!==generation||!playing||paused)return;try{const nextState=await requestState('/api/snake/tick',{direction:pendingDirection,state});if(token!==generation)return;state=nextState;pendingDirection=null;draw();if(state.over){playing=false;showOverlay(state.won?'Perfect board':'Game over',`Score ${state.score}`,ai?'Run again':'Try again');setStatus(state.won?'Perfect board':`Game over · score ${state.score}`);return;}setStatus(`${ai?'AI running':'Playing'} · score ${state.score} · Python engine`);schedule(token);}catch{if(token!==generation)return;playing=false;showOverlay('Connection paused','The Python game engine could not be reached.','Restart');setStatus('Could not reach Python engine');}};
    const start=()=>{overlay.hidden=true;playing=true;paused=false;pause.textContent='Pause';const token=++generation;setStatus(`${ai?'AI running':'Playing'} · Python engine`);schedule(token);};
    const reset=async()=>{generation++;clearTimeout(timer);playing=false;paused=false;pendingDirection=null;pause.textContent='Pause';setStatus('Starting Python game');try{state=await requestState('/api/snake/new',{ai});draw();showOverlay(ai?'Snake AI':'Snake',ai?'Running Hamiltonian shortcut logic.':'Play on a 20 × 20 grid.',ai?'Run AI':'Start');setStatus('Ready · Python engine');}catch{showOverlay('Connection paused','The Python game engine could not be reached.','Retry');setStatus('Could not reach Python engine');}modePlay.classList.toggle('primary-button',!ai);modeAI.classList.toggle('primary-button',ai);};
    const changeMode=nextAI=>{ai=nextAI;reset();};
    const setDirection=direction=>{if(!ai)pendingDirection=direction;};
    const togglePause=()=>{if(!playing)return;paused=!paused;pause.textContent=paused?'Resume':'Pause';setStatus(paused?'Paused':`${ai?'AI running':'Playing'} · Python engine`);if(!paused)schedule(generation);};
    overlay.querySelector('button').addEventListener('click',()=>state?start():reset());
    root.querySelectorAll('[data-dir]').forEach(control=>control.addEventListener('click',()=>setDirection(control.dataset.dir)));
    window.addEventListener('keydown',event=>{const directions={ArrowUp:'up',w:'up',ArrowDown:'down',s:'down',ArrowLeft:'left',a:'left',ArrowRight:'right',d:'right'};if(directions[event.key]){event.preventDefault();setDirection(directions[event.key]);}if(event.code==='Space'){event.preventDefault();togglePause();}if(event.key.toLowerCase()==='r')reset();});
    restart=reset;draw();reset();
  }

  const games = {'connect-four':connectFourPython,snake:snakeGamePython,hangman,'rubiks-cube':rubiksCube3D,'space-invaders':spaceInvaders,'tic-tac-toe':ticTacToePython,'sorting-lab':sortingLab,'pathfinding-lab':pathfindingLab};
  const game = games[document.body.dataset.game];
  if (game) game(); else root.textContent = 'This project could not be loaded.';
})();
