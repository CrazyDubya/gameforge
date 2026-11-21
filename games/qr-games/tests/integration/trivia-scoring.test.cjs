// Run with Node >=18: node --test tests/integration/trivia-scoring.test.cjs
// Actual handler/game/storage modules; only socket transport and Redis client
// are fakes. No server, external Redis, network or provider is started.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
// Fail closed if an imported module attempts a network connection.
const net = require('node:net');
net.Socket.prototype.connect = function () { throw new Error('Network forbidden in scoring regression'); };
const source = process.env.QR_SOURCE || path.resolve(__dirname, '../..');
const setup = require(path.join(source,'src/sockets/game.js'));
const {MemoryStorage,RedisStorage} = require(path.join(source,'src/utils/storage.js'));

async function fixture(kind) {
 const values=new Map();
 const storage=kind==='memory'?new MemoryStorage():new RedisStorage({
   get:async key=>values.get(key)||null,
   set:async(key,value)=>{values.set(key,value);return 'OK';}
 });
 const sent=[];
 const io={to:room=>({emit:(event,data)=>sent.push({room,event,data})})};
 function socket(id){const handlers={};setup({id,on:(name,fn)=>{handlers[name]=fn;},emit:(event,data)=>sent.push({to:id,event,data})},io,storage);return handlers;}
 const host=socket('host'),alice=socket('alice'),bob=socket('bob'),outsider=socket('outsider');
 await storage.set('fixture01',{id:'fixture01',hostSocketId:'host',players:[{id:'alice',name:'Alice'},{id:'bob',name:'Bob'}]});
 const start=()=>host['start-game']({lobbyId:'fixture01',gameType:'trivia'});
 const answer=(client,value)=>client['submit-answer']({lobbyId:'fixture01',answer:value});
 const scores=async()=> (await storage.get('fixture01')).players.map(p=>p.score);
 await start();
 return {storage,host,alice,bob,outsider,sent,start,answer,scores};
}
for(const kind of ['memory','redis-json-client']){
 test(kind+': repeated correct answer awards once and preserves feedback',async()=>{
  const f=await fixture(kind);
  await f.answer(f.alice,'Paris');assert.deepEqual(await f.scores(),[1,0]);
  await f.answer(f.alice,'Paris');assert.deepEqual(await f.scores(),[1,0]);
  assert.equal(f.sent.filter(x=>x.event==='answer-result').length,2);
 });
 test(kind+': two players have independent eligibility',async()=>{
  const f=await fixture(kind);await f.answer(f.alice,'Paris');await f.answer(f.bob,'Paris');
  await f.answer(f.alice,'Paris');await f.answer(f.bob,'Paris');assert.deepEqual(await f.scores(),[1,1]);
 });
 test(kind+': next question earns a new point only once',async()=>{
  const f=await fixture(kind);await f.answer(f.alice,'Paris');await f.host['next-question']('fixture01');
  await f.answer(f.alice,'4');await f.answer(f.alice,'4');assert.deepEqual(await f.scores(),[2,0]);
 });
 test(kind+': wrong-then-correct retry stays allowed, no repeated credit',async()=>{
  const f=await fixture(kind);await f.answer(f.alice,'Berlin');assert.deepEqual(await f.scores(),[0,0]);
  await f.answer(f.alice,'Paris');await f.answer(f.alice,'Paris');assert.deepEqual(await f.scores(),[1,0]);
 });
 test(kind+': restart resets scores and eligibility',async()=>{
  const f=await fixture(kind);await f.answer(f.alice,'Paris');await f.start();assert.deepEqual(await f.scores(),[0,0]);
  await f.answer(f.alice,'Paris');await f.answer(f.alice,'Paris');assert.deepEqual(await f.scores(),[1,0]);
 });
 test(kind+': nonmember cannot score',async()=>{
  const f=await fixture(kind);await f.answer(f.outsider,'Paris');assert.deepEqual(await f.scores(),[0,0]);
  assert.equal(f.sent.filter(x=>x.event==='answer-result').length,0);
 });
 test(kind+': wrong answers never earn points',async()=>{
  const f=await fixture(kind);await f.answer(f.alice,'Berlin');await f.answer(f.alice,'Berlin');
  assert.deepEqual(await f.scores(),[0,0]);
 });
 test(kind+': delayed wrong answer does not remove earned score',async()=>{
  const f=await fixture(kind);await f.answer(f.alice,'Paris');await f.answer(f.alice,'Berlin');
  await f.answer(f.alice,'Paris');assert.deepEqual(await f.scores(),[1,0]);
 });
 test(kind+': legacy missing tracking starts safely without score reset',async()=>{
  const f=await fixture(kind);const l=await f.storage.get('fixture01');delete l.gameState.awardedAnswers;
  l.players[0].score=4;await f.storage.set('fixture01',l);
  await f.answer(f.alice,'Paris');await f.answer(f.alice,'Paris');assert.deepEqual(await f.scores(),[5,0]);
 });
}
