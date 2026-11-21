/** Real shipped-schema restore checks. Run: tsx --test tests/regression/restore-atomicity.test.ts
 * Requires Node22 SQLite, tsx and the project's nanoid. SAVE_SOURCE_ROOT selects baseline.
 */
import { DatabaseSync } from 'node:sqlite';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { test } from 'node:test';
import assert from 'node:assert/strict';
const root=resolve(fileURLToPath(new URL('../..',import.meta.url)));
const source=process.env.SAVE_SOURCE_ROOT ?? root;
const {SaveDataLoader}=await import(pathToFileURL(resolve(source,'src/game/saves/loader.ts')).href);
const {SaveDataSerializer}=await import(pathToFileURL(resolve(source,'src/game/saves/serializer.ts')).href);
const schema=readFileSync(process.env.SAVE_SCHEMA ?? resolve(root,'migrations/apply_all.sql'),'utf8');

function setup(){
 const db=new DatabaseSync(':memory:');db.exec(schema);
 db.exec("INSERT INTO characters(id,player_id,legal_name,current_health)VALUES('a','p','Synthetic A',80),('b','q','Synthetic B',90)");
 db.exec("INSERT INTO item_definitions(id,code,name)VALUES('item-a','SYNTH_A','Synthetic A')");
 db.exec("INSERT INTO character_inventory(id,character_id,item_definition_id,quantity)VALUES('inv-a','a','item-a',2),('inv-b','b','item-a',3)");
 const category=(db.prepare('SELECT value FROM enum_attribute_category LIMIT 1').get() as any).value;
 db.prepare('INSERT INTO attribute_definitions(id,code,name,abbreviation,category)VALUES(?,?,?,?,?)').run('attr','SYNTH_ATTR','Synthetic','SYN',category);
 db.exec("INSERT INTO character_attributes(id,character_id,attribute_id,base_value,current_value)VALUES('ca','a','attr',5,5)");
 const log:any[]=[];let batches=0;
 function prepare(sql:string,params:any[]=[]):any{return {sql,params,bind(...p:any[]){return prepare(sql,p)},async first(){return db.prepare(sql).get(...params)??null},async all(){return {results:db.prepare(sql).all(...params)}},async run(){log.push({sql:sql.replace(/\s+/g,' ').trim(),params});return db.prepare(sql).run(...params)}};}
 const adapter={prepare,async batch(statements:any[]){batches++;db.exec('BEGIN');try{const out=[];for(const stmt of statements)out.push(await stmt.run());db.exec('COMMIT');return out}catch(e){db.exec('ROLLBACK');throw e}}};
 return {db,adapter,log,get batches(){return batches},loader:new SaveDataLoader(adapter),serializer:new SaveDataSerializer(adapter)};
}
async function saved(x:ReturnType<typeof setup>){const chunk=await x.serializer.serializeCharacterCore('a','save');const character=JSON.parse(chunk.data);character.current_health=25;return {success:true,restoredData:{character,inventory:null,skills:null,reputation:null}};}
function state(x:ReturnType<typeof setup>){return {characters:x.db.prepare('SELECT id,current_health FROM characters ORDER BY id').all(),inventory:x.db.prepare('SELECT id,character_id,item_definition_id,quantity FROM character_inventory ORDER BY id').all(),attributes:x.db.prepare('SELECT id,current_value FROM character_attributes ORDER BY id').all()};}
const attr={attribute_id:'attr',base_value:7,current_value:7,bonus_from_augments:0,bonus_from_items:0,bonus_from_conditions:0,temporary_modifier:0,times_increased:1,xp_invested:20};

test('core-only restore succeeds with intended value',async()=>{const x=setup();try{const result=await x.loader.restoreCharacterState('a',await saved(x));assert.equal(result.restored,true);assert.deepEqual(result.changes,['character_core']);assert.equal((x.db.prepare("SELECT current_health FROM characters WHERE id='a'").get()as any).current_health,25);}finally{x.db.close()}});
test('core and attributes restore successfully',async()=>{const x=setup();try{const result:any=await saved(x);result.restoredData.skills={attributes:[attr]};await x.loader.restoreCharacterState('a',result);assert.equal((x.db.prepare("SELECT current_value FROM character_attributes WHERE id='ca'").get()as any).current_value,7);if(process.env.SAVE_TRACE)writeFileSync(process.env.SAVE_TRACE,JSON.stringify({log:x.log,state:state(x),batches:x.batches},null,2));}finally{x.db.close()}});
test('unsuccessful result makes no writes',async()=>{const x=setup();try{const before=state(x);const result:any=await saved(x);result.success=false;assert.equal((await x.loader.restoreCharacterState('a',result)).restored,false);assert.deepEqual(state(x),before);assert.equal(x.log.length,0);}finally{x.db.close()}});
test('missing core makes no writes',async()=>{const x=setup();try{const before=state(x);const result:any=await saved(x);result.restoredData.character=null;assert.equal((await x.loader.restoreCharacterState('a',result)).restored,false);assert.deepEqual(state(x),before);}finally{x.db.close()}});
test('actual inventory schema error does not partially restore or delete',async()=>{const x=setup();try{const before=state(x),result:any=await saved(x);result.restoredData.inventory={items:[{id:'saved-inv',item_id:'item-a',quantity:1,is_equipped:0,equipped_slot:null,durability_current:null,durability_max:null,custom_name:null,acquired_from:null,acquired_at:'2026-01-01'}]};await assert.rejects(x.loader.restoreCharacterState('a',result),/item_id/);assert.deepEqual(state(x),before);}finally{x.db.close()}});
test('late SQLite constraint failure rolls back earlier core and inventory writes',async()=>{const x=setup();try{x.db.exec("CREATE TRIGGER reject_attr BEFORE UPDATE ON character_attributes BEGIN SELECT RAISE(ABORT,'synthetic late failure'); END");const before=state(x),result:any=await saved(x);result.restoredData.inventory={items:[]};result.restoredData.skills={attributes:[attr]};await assert.rejects(x.loader.restoreCharacterState('a',result),/synthetic late failure/);assert.deepEqual(state(x),before);}finally{x.db.close()}});
test('successful empty inventory still deletes only intended character rows',async()=>{const x=setup();try{const result:any=await saved(x);result.restoredData.inventory={items:[]};await x.loader.restoreCharacterState('a',result);assert.equal((x.db.prepare("SELECT count(*) AS n FROM character_inventory WHERE character_id='a'").get()as any).n,0);assert.equal((x.db.prepare("SELECT count(*) AS n FROM character_inventory WHERE character_id='b'").get()as any).n,1);}finally{x.db.close()}});
test('repeating successful restore retains same resulting state',async()=>{const x=setup();try{const result=await saved(x);await x.loader.restoreCharacterState('a',result);const before=state(x);await x.loader.restoreCharacterState('a',result);assert.deepEqual(state(x),before);}finally{x.db.close()}});
test('unrelated character stays unchanged',async()=>{const x=setup();try{await x.loader.restoreCharacterState('a',await saved(x));assert.equal((x.db.prepare("SELECT current_health FROM characters WHERE id='b'").get()as any).current_health,90);}finally{x.db.close()}});
