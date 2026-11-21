// Real-browser regression for narrative-follow intent. No backend or model calls.
// The actual class is parsed intact; only its selected methods are initialized.
// Geometry-only fixture, not full-page UI or constructor integration coverage.
// Install playwright-core temporarily outside this repository, then run:
// NODE_PATH=/tmp/ui-test-deps/node_modules node tests/ui/test_smart_scroll.cjs
// CHROME_EXECUTABLE optionally names an existing Chrome/Chromium binary.
// Optional first argument selects another template (e.g. a baseline copy).
// SCROLL_TEST_ARTIFACTS optionally saves result JSON and screenshots.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');
const template = process.argv[2] || path.resolve(__dirname, '../../living_rusted_tankard/game/templates/enhanced_game.html');
const artifacts = process.env.SCROLL_TEST_ARTIFACTS || null;
if (artifacts) fs.mkdirSync(artifacts, {recursive:true});
const html = fs.readFileSync(template,'utf8');
const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const classScript = scripts.find(s=>s.includes('class EnhancedGameInterface'));
if(!classScript) throw Error('actual class missing');
(async()=>{
 const browser = await chromium.launch({executablePath:process.env.CHROME_EXECUTABLE || '/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
 const page = await browser.newPage({viewport:{width:1000,height:760}});
 const network = [];
 await page.route('**/*',route=>{network.push(route.request().url());return route.abort();});
 await page.setContent(html.replace(/<script(?:\s[^>]*)?>[\s\S]*?<\/script>/g,'').replace(/<link[^>]*>/g,''));
 await page.addStyleTag({content:`
  body {font:18px Arial;background:#111827;color:#e5e7eb;}
  body * {visibility:hidden;}
  #narrative-content,#narrative-content * {visibility:visible;}
  #narrative-content {position:fixed!important;top:100px!important;left:80px!important;width:800px!important;height:480px!important;overflow-y:scroll!important;background:#182334;padding:12px;box-sizing:border-box;border:2px solid #d68c0a;scroll-behavior:auto!important;overflow-anchor:none!important;}
  #narrative-content>div {display:block;animation:none!important;line-height:24px;padding:8px;border-bottom:1px solid #40516b;white-space:pre-line;}
  #fixture-label {visibility:visible!important;position:fixed;top:20px;left:80px;font-size:20px;max-width:800px;}
 `});
 await page.addScriptTag({content:classScript+'\nwindow.TestInterface=EnhancedGameInterface;'});
 await page.evaluate(()=>{
  window.subject=Object.create(window.TestInterface.prototype);
  subject.elements={narrativeContent:document.getElementById('narrative-content'),scrollToBottomBtn:document.getElementById('scroll-to-bottom-btn')};
  subject.scrollTicking=false;
  const label=document.createElement('div');label.id='fixture-label';document.body.appendChild(label);
 });
 const cases=[];
 for(const item of [
  {name:'bottom_tall_incoming',atBottom:true,tall:true,player:false,wantBottom:true},
  {name:'near_bottom_tall_incoming',atBottom:true,offset:50,tall:true,player:false,wantBottom:true},
  {name:'boundary_100px_history',atBottom:true,offset:100,tall:true,player:false,wantBottom:false},
  {name:'user_scrolls_back_during_delay',atBottom:true,tall:true,player:false,scrollBack:true,wantBottom:false},
  {name:'bottom_short_incoming',atBottom:true,tall:false,player:false,wantBottom:true},
  {name:'history_tall_incoming',atBottom:false,tall:true,player:false,wantBottom:false},
  {name:'history_player_forced',atBottom:false,tall:true,player:true,wantBottom:true},
  {name:'explicit_button_equivalent_force',atBottom:false,tall:false,force:true,wantBottom:true}
 ]){
  const before=await page.evaluate(item=>{
   const el=subject.elements.narrativeContent;
   el.innerHTML='';for(let i=0;i<35;i++){const d=document.createElement('div');d.textContent='History '+i+': a synthetic line for scroll positioning.';el.appendChild(d);}
   el.scrollTop=item.atBottom?el.scrollHeight:200;
   if(item.offset)el.scrollTop-=item.offset;
   document.getElementById('fixture-label').textContent=(item.name+' | actual repository class, isolated geometry fixture');
   return {top:el.scrollTop,height:el.scrollHeight,client:el.clientHeight};
  },item);
  await page.evaluate(item=>{
   if(item.force)subject.scrollToBottom(true);
   else subject.addNarrative(item.tall?Array.from({length:14},(_,i)=>'New response line '+i+' to test long-message following.').join('\n'):'A short new response.',!!item.player);
     if(item.scrollBack)subject.elements.narrativeContent.scrollTop=200;
  },item);
  await page.waitForTimeout(200);
  const after=await page.evaluate(()=>{const e=subject.elements.narrativeContent;return {top:e.scrollTop,height:e.scrollHeight,client:e.clientHeight,gap:e.scrollHeight-e.scrollTop-e.clientHeight};});
  const passed=item.wantBottom?after.gap<=2:Math.abs(after.top-(item.scrollBack?200:before.top))<=2;
  cases.push({...item,before,after,passed});
  if(artifacts && (item.name==='bottom_tall_incoming'||item.name==='history_tall_incoming'))await page.screenshot({path:path.join(artifacts,item.name+'.png')});
 }
 await browser.close();
 const result={template,cases,network_attempts:network,passed:cases.filter(c=>c.passed).length,total:cases.length,scope:'actual full class methods and real DOM, test-only fixed geometry; no constructor/backend/full-page appearance parity'};
 if (artifacts) fs.writeFileSync(path.join(artifacts,'results.json'),JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify(result,null,2));
 if(cases.some(c=>!c.passed)||network.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
