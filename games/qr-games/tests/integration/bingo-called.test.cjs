const {test}=require('node:test');
const assert=require('node:assert/strict');
const path=require('node:path');
require('node:net').Socket.prototype.connect=function(){throw Error('Network forbidden');};
const source=process.env.QR_SOURCE||path.resolve(__dirname,'../..');
const setup=require(path.join(source,'src/sockets/game.js'));
const {MemoryStorage,RedisStorage}=require(path.join(source,'src/utils/storage.js'));
async function fixture(kind){
 const values=new Map();const storage=kind==='memory'?new MemoryStorage():new RedisStorage({get:async k=>values.get(k)||null,set:async(k,v)=>{values.set(k,v);return 'OK';}});
 const sent=[];const io={to:room=>({emit:(event,data)=>sent.push({room,event,data})})};
 function socket(id){const h={};setup({id,on:(n,f)=>{h[n]=f;},emit:(event,data)=>sent.push({to:id,event,data})},io,storage);return h;}
 const player=socket('alice'),outsider=socket('outsider');
 const card=Array.from({length:5},(_,row)=>Array.from({length:5},(_,col)=>({value:row===2&&col===2?'FREE':col*15+row+1,marked:row===2&&col===2})));
 const lobby={id:'fixture01',gameType:'bingo',gameState:{calledNumbers:[],patterns:['single-line']},players:[{id:'alice',name:'Alice',bingoCard:card}]};await storage.set(lobby.id,lobby);
 const mark=(number,client=player)=>client['mark-number']({lobbyId:lobby.id,number});
 const claim=()=>player['claim-bingo']({lobbyId:lobby.id,pattern:'single-line'});
 const get=()=>storage.get(lobby.id);
 return {storage,sent,player,outsider,lobby,mark,claim,get};
}
for(const kind of ['memory','redis-json-client']){
 test(kind+': uncalled numbers cannot be marked into a winning row',async()=>{
  const f=await fixture(kind);for(const n of [1,16,31,46,61])await f.mark(n);await f.claim();
  assert.equal(f.sent.filter(x=>x.event==='bingo-winner').length,0);
  assert.deepEqual((await f.get()).players[0].bingoCard[0].map(c=>c.marked),[false,false,false,false,false]);
 });
 test(kind+': called row marks and wins',async()=>{
  const f=await fixture(kind);const l=await f.get();l.gameState.calledNumbers=[1,16,31,46,61];await f.storage.set(l.id,l);
  for(const n of l.gameState.calledNumbers)await f.mark(n);await f.claim();assert.equal(f.sent.filter(x=>x.event==='bingo-winner').length,1);
 });
 test(kind+': uncalled numeric card cell stays unmarked and no acknowledgment',async()=>{
  const f=await fixture(kind);await f.mark(1);assert.equal((await f.get()).players[0].bingoCard[0][0].marked,false);assert.equal(f.sent.filter(x=>x.event==='number-marked').length,0);
 });
 test(kind+': FREE remains marked without needing a call',async()=>{
  const f=await fixture(kind);await f.mark('FREE');assert.equal((await f.get()).players[0].bingoCard[2][2].marked,true);
 });
 test(kind+': called value not on card cannot change card',async()=>{
  const f=await fixture(kind);const l=await f.get();l.gameState.calledNumbers=[15];await f.storage.set(l.id,l);const before=JSON.stringify(l.players[0].bingoCard);await f.mark(15);assert.equal(JSON.stringify((await f.get()).players[0].bingoCard),before);
 });
 test(kind+': nonmember cannot mark another player card',async()=>{
  const f=await fixture(kind);const l=await f.get();l.gameState.calledNumbers=[1];await f.storage.set(l.id,l);await f.mark(1,f.outsider);assert.equal((await f.get()).players[0].bingoCard[0][0].marked,false);
 });
 test(kind+': wrong game cannot mark',async()=>{
  const f=await fixture(kind);const l=await f.get();l.gameType='trivia';l.gameState.calledNumbers=[1];await f.storage.set(l.id,l);await f.mark(1);assert.equal((await f.get()).players[0].bingoCard[0][0].marked,false);
 });
}
