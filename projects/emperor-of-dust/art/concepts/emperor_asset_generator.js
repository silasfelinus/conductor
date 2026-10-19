const fs = require('fs');
const path = require('path');
const OUTPUT = '/mnt/data/emperor-of-dust-concepts';
const C={ink:'#211d23',dark:'#161f2b',deep:'#0e1820',cream:'#efdbb0',paper:'#d5b780',sand:'#bc8d5d',ochre:'#aa633b',copper:'#dd9b55',brass:'#d8b56f',rust:'#814c41',sage:'#718679',water:'#708b87',fog:'#d8c4ab',red:'#bb6554'};
const wrap=(inner,w=1600,h=1000,defs='')=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="Emperor of Dust concept artwork"><defs><linearGradient id="paper" x2="0.9" y2="1"><stop stop-color="#edd5ab"/><stop offset=".52" stop-color="#cfac77"/><stop offset="1" stop-color="#997255"/></linearGradient><linearGradient id="night" x2=".8" y2="1"><stop stop-color="#142c36"/><stop offset=".65" stop-color="#253743"/><stop offset="1" stop-color="#7a4f41"/></linearGradient><linearGradient id="amber" x2=".15" y2="1"><stop stop-color="#f4ce83"/><stop offset="1" stop-color="#ad6943"/></linearGradient><radialGradient id="lamp"><stop stop-color="#ffe5a5" stop-opacity=".68"/><stop offset="1" stop-color="#dd9150" stop-opacity="0"/></radialGradient><pattern id="hatch" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(25)"><path d="M0 0V12" stroke="#3c3030" stroke-opacity=".19" stroke-width="2"/></pattern><pattern id="grain" width="29" height="23" patternUnits="userSpaceOnUse"><circle cx="3" cy="6" r="1.1" fill="#392923" opacity=".22"/><path d="M17 12l3 2M24 3l1 3" stroke="#40342f" stroke-opacity=".2"/></pattern><pattern id="screws" width="48" height="48" patternUnits="userSpaceOnUse"><circle cx="24" cy="24" r="2.4" fill="#d4ad71"/><path d="M21 24h6" stroke="#372c2b" stroke-width="1"/></pattern><filter id="soft"><feGaussianBlur stdDeviation="11"/></filter>${defs}</defs>${inner}</svg>`;
const T=(x,y,str,size=22,color=C.ink,anchor='start',extra='')=>`<text x="${x}" y="${y}" font-family="Georgia,serif" font-size="${size}" font-weight="${size>=30?'bold':'normal'}" letter-spacing="${size>=30?2:0.5}" text-anchor="${anchor}" fill="${color}" ${extra}>${str}</text>`;
const R=(x,y,w,h,fill,stroke=C.ink,sw=2,rx=0)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
const P=(d,fill='none',stroke=C.ink,sw=3,other='')=>`<path d="${d}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round" stroke-linecap="round" ${other}/>`;
const E=(x,y,rx,ry,fill,stroke=C.ink,sw=2)=>`<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
const line=(x,y,X,Y,stroke=C.ink,sw=2,dash='')=>`<path d="M${x} ${y}L${X} ${Y}" stroke="${stroke}" stroke-width="${sw}" ${dash?`stroke-dasharray="${dash}"`:''} fill="none"/>`;
function prng(seed){return ()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;}}
const random=prng(1337);
function esc(s){return s.replaceAll('&','&amp;').replaceAll('<','&lt;')}
function house(x,y,s=1,fill='#a98562'){return `<g transform="translate(${x},${y}) scale(${s})">${R(-21,-10,42,29,fill,C.ink,3)}${P('M-28 -10L0 -34L28 -10Z','#6a4941',C.ink,3)}${R(-6,0,12,19,'#3d3431',C.ink,1)}${R(-15,-1,7,8,'#efcb83',C.ink,1)}${line(-24,20,24,20,C.ink,3)}</g>`}
function tower(x,y,s=1){return `<g transform="translate(${x},${y}) scale(${s})">${P('M-44 30L-37 -36L36 -36L43 30Z','#8d7565',C.ink,4)}${R(-31,-72,62,37,'#8b7064',C.ink,4)}${P('M-42 -72L-44 -95L-27 -95L-27 -85L-10 -85L-10 -95L8 -95L8 -85L25 -85L25 -95L42 -95L40 -72Z','#594d48',C.ink,4)}${R(-8,-53,17,29,'#d9b87d',C.ink,3,7)}${R(-10,-6,20,36,'#282c2e',C.ink,3,9)}${line(-33,-21,33,-21,'#403b3a',3)}</g>`}
function bell(x,y,s=1){return `<g transform="translate(${x},${y}) scale(${s})">${house(0,9,.75,'#b08e70')}${P('M-12 -15L-12 -67L12 -67L12 -15Z','#aa8060',C.ink,3)}${P('M-18 -67L0 -83L18 -67Z','#624a43',C.ink,3)}${P('M-8 -53Q0 -60 8 -53L12 -39Q0 -29 -12 -39Z','#d9b46c',C.ink,2)}${E(0,-38,3,3,C.ink)}</g>`}
function marsh(x,y,s=1){let o=`<g transform="translate(${x},${y}) scale(${s})">`;for(let i=0;i<14;i++){const xx=i*19-122,yy=(i%4)*11;o+=P(`M${xx} ${yy+20}q-7 -20 -3 -37M${xx} ${yy+22}q10 -25 14 -33`, 'none','#45625a',2);o+=E(xx+3,yy+22,10,2,'#7d9583','none',0);}return o+'</g>'}
function ridge(x,y,s=1){return `<g transform="translate(${x},${y}) scale(${s})">${P('M-100 82L-33 -83L16 -22L48 -111L110 78Z','#665f5c',C.ink,4)}${P('M-95 82L-28 -67L-4 -20L-28 2L35 78Z','#9d806b','#514641',2)}${P('M48 -111L40 -56L53 -61L110 78','#4e5053',C.ink,3)}${P('M-22 17l-37 59M70 -3l23 77M36 10l-13 56','none','#4e4b4b',3)}</g>`}
function canyon(x,y,s=1){return `<g transform="translate(${x},${y}) scale(${s})">${P('M-210 -12Q-100 -76 10 -23T215 -24L220 96Q90 29 10 90T-210 73Z','#9d6348','#6c4439',3)}${P('M-207 3Q-105 -48 10 4T209 4','none','#d9a26d',7)}${P('M-207 17Q-100 -33 10 19T215 18','none','#5e423a',4)}${P('M-207 29Q-100 -13 10 40T215 39','none','#ca9b6b',2)}${P('M-191 -2Q-100 -48 10 5T193 5','none','#392f31',2,'stroke-dasharray="11 11"')}</g>`}
function mapBase(labelled=false, overlay=false){let s='';if(overlay){s+=`<rect width="1600" height="1000" fill="none"/>${P('M1050 190Q1160 260 1110 365T860 410L720 510','none','#cd6b66',16,'opacity=".62"')}${P('M1115 365L1200 423M1000 420L1040 490M915 401L882 334','none','#efc9a1',8,'opacity=".75"')}${P('M540 580L820 540L1120 544','none','#b44d41',7,'stroke-dasharray="28 19"')}${P('M800 250L785 420','none','#a73c32',12,'opacity=".32"')}${T(900,83,'DAY 41 · THE BROKEN REIGN',42,C.cream,'middle')}`;return wrap(s)}
s+=R(0,0,1600,1000,'url(#paper)','none',0)+R(0,0,1600,1000,'url(#grain)','none',0)+R(25,25,1550,950,'none','#473a33',12,16)+R(41,41,1518,918,'none','#b58d5e',3,5);
s+=P('M65 90Q175 120 270 95T510 105T720 103T1000 106T1250 91T1530 112L1530 910Q1300 924 1130 911T710 921T265 914L65 911Z','#d6b78a','none',0);
s+=P('M65 135Q160 220 275 250T360 510L305 635L66 740Z','#8b8272','none',0);s+=P('M70 180L235 180L310 320L210 470L80 495Z','url(#hatch)','none',0);
s+=P('M395 115Q550 72 710 119T1040 145L1150 260Q1085 337 940 298T640 310T395 235Z','#8d9b88','#566a60',5);s+=P('M395 115Q550 72 710 119T1040 145L1150 260Q1085 337 940 298T640 310T395 235Z','url(#hatch)','none',0);
s+=P('M1318 102Q1450 90 1535 107L1532 640Q1430 558 1345 610L1285 344Z','#525c59','#393d3b',3);s+=P('M1318 102Q1450 90 1535 107L1532 640Q1430 558 1345 610L1285 344Z','url(#hatch)','none',0);
s+=P('M280 605Q435 571 600 628L770 805L330 886L91 850Z','#bb9167','#815d49',2);s+=P('M265 610Q455 600 630 657L740 810L320 880L91 853Z','url(#hatch)','none',0);
s+=P('M810 720L1460 675L1510 922L880 921Z','#988776','#6b6258',3);s+=P('M810 720L1460 675L1510 922L880 921Z','url(#hatch)','none',0);
s+=P('M660 150Q720 225 810 320Q927 415 950 512Q1020 640 1030 700L1010 880','none','#698f89',24,'opacity=".64"');s+=P('M660 150Q720 225 810 320Q927 415 950 512Q1020 640 1030 700L1010 880','none','#d6e0be',6,'opacity=".6"');
// Saltroad, mission road, and aqueduct
s+=P('M110 777Q245 703 320 641L515 545L835 535L1040 545L1294 376','none','#6b4c3e',19);s+=P('M110 777Q245 703 320 641L515 545L835 535L1040 545L1294 376','none','#e0c18b',12);s+=P('M815 373L1131 215','none','#8e684b',12);s+=P('M815 373L1131 215','none','#edd1a0',7);s+=P('M875 330Q1020 262 1185 326L1345 362','none','#7d786a',10);s+=P('M875 330Q1020 262 1185 326L1345 362','none','#d8ca9d',5,'stroke-dasharray="14 7"');
s+=P('M465 665Q540 719 650 753L798 767','none','#463936',5,'stroke-dasharray="6 15"');
// Terrain landmarks
for(let i=0;i<4;i++)s+=ridge(122+i*59,270+(i%2)*115,.55+(i%3)*.06);
s+=marsh(560,192,.68)+marsh(810,178,.61)+marsh(983,224,.44);
for(let i=0;i<11;i++){let x=365+i*34, y=730+(i%3)*26;s+=P(`M${x} ${y+46}l10 -${45+i%3*12}l20 ${30+i%4*5}l4 28Z`,'#956d51',C.ink,2);}
for(let i=0;i<8;i++){let x=1430+(i%3)*28,y=140+i*48;s+=P(`M${x} ${y+35}l-17 -2l14 -23l-9 -1l10 -23l9 23l-7 1l14 25Z`,'#354a48',C.ink,2)}
s+=canyon(875,800,.75);
for(let i=0;i<7;i++){let x=1240+i*37,y=750+(i%2)*58;s+=R(x,y,45,16,'#66554e',C.ink,2,4)+line(x+3,y+5,x+41,y+5,'#d4af73',2);}
s+=E(148,817,105,26,'#dcd0a8','#987f61',3);for(let i=0;i<9;i++)s+=line(85+i*17,820,132+i*17,808,'#a99c79',2);
s+=E(550,366,58,35,'#526f6c','#344e4e',5)+E(550,366,43,21,'#b6c4a3','#344e4e',2);for(let i=0;i<6;i++)s+=P(`M${510+i*16} 326l7 -32l12 26`,'none','#393c3a',5);
// Key settlements and mesa
s+=E(810,399,142,64,'#86684f','#43372f',7)+E(810,388,121,42,'#b79a70','#463c35',4)+tower(810,375,1.05);
s+=bell(1345,372,1.1)+bell(1120,247,.75);
for (const [x,y,sc] of [[422,530,.8],[478,552,.57],[612,533,.62],[697,562,.68],[1104,562,.72],[1170,626,.65],[1245,629,.54],[1061,502,.56]])s+=house(x,y,sc);
s+=house(1136,683,.72,'#b4956c')+house(1191,704,.65,'#b4956c')+house(1212,676,.53,'#b4956c');
for(let i=0;i<5;i++)s+=P(`M${690+i*29} ${821+i%2*6}l-12 -24l26 -1l9 24Z`,'#8d5042','#382d2e',3);
// compass and scale
s+=E(1460,815,74,74,'#d3b187','#584333',3)+P('M1460 751l14 63l-14 61l-14 -61Z','#533c36','#3c3030',3)+P('M1399 814l61 -14l61 14l-61 14Z','#e5c998','#3c3030',2)+T(1460,743,'N',26,C.ink,'middle')+T(1460,909,'S',18,C.ink,'middle');
if(labelled){
s+=R(330,35,940,73,'#241e20','#ab805b',3,7)+T(800,84,'EMPEROR OF DUST · THE WASTELAND',39,C.cream,'middle');
const labels=[
[194,180,'STORM CROW','HEIGHTS'],[710,141,'MIREFEN','WETLANDS'],[1120,145,'SILENT BELL','ABBEY'],[1430,178,'BLACK','VERGE'],[530,423,'BLACK STONES','WATERING HOLE'],[806,484,'THE','FORTRESS'],[1350,459,'HOLLOW BELL',''],[500,624,'SALTROAD',''],[1040,610,'EASTERN FORD',''],[1180,753,'THISTLEDOWN',''],[484,848,'THE BADLANDS',''],[872,925,'JACKALWIRE','RAIL CANYON'],[1320,890,'SUNKEN','RAIL YARDS'],[165,906,'SALT FLATS','']];
for(const [x,y,a,b] of labels){const wide=Math.max(130,a.length*11,b.length*10);s+=R(x-wide/2-7,y-21,wide+14,b?50:30,'#2f2a28','#b88b58',1,4);s+=T(x,y,a,19,C.cream,'middle');if(b)s+=T(x,y+22,b,16,C.cream,'middle');}
// day-1 fog, intentionally transparent
s+=P('M1250 100Q1380 105 1532 94L1532 622Q1470 581 1390 596L1373 418Q1445 310 1250 100Z','#d9d0bb','none',0,'opacity=".47"');s+=P('M1150 735Q1320 670 1525 650L1525 925L1130 924Z','#ddd0ba','none',0,'opacity=".5"');
s+=R(68,925,650,38,'#281f20','#a78258',2,4)+T(88,950,'DAY 1   •   FOG OF WAR: RUSTLINE &amp; BLACK VERGE',17,C.cream);
}else{s+=R(70,38,300,46,'#201e1c','#ad8c5e',2,5)+T(220,68,'UNLABELLED ART BASE',20,C.cream,'middle');}
return wrap(s);
}
function fortress(labelled=false){let s=R(0,0,1600,1000,'url(#night)','none',0)+E(1170,280,540,410,'url(#lamp)','none',0)+P('M0 615Q170 585 300 648T620 622T900 610T1300 666T1600 620L1600 1000L0 1000Z','#594e49','none',0)+R(0,0,1600,1000,'url(#grain)','none',0);
// mesa and fortress base
s+=P('M155 760L347 715L1249 703L1510 769L1470 945L204 947Z','#7c5947',C.ink,9)+P('M210 780L1397 768L1450 854L190 856Z','#a58060','#372d2e',4);
s+=P('M575 186L634 126L1025 126L1076 185Z','#574345',C.ink,6)+R(610,179,445,490,'#967559',C.ink,7)+R(633,195,400,475,'#322e32',C.ink,4);
// upper map room
s+=R(644,208,378,149,'#5c6260','#dec18e',3)+R(670,227,85,97,'#292d35','#b79461',5,24)+R(899,227,85,97,'#29343b','#b79461',5,24)+P('M696 298Q714 266 739 274','none','#c5a86f',4)+P('M915 291Q945 256 968 280','none','#c5a86f',4);
s+=P('M752 315L898 306L937 342L717 342Z','#b89a75','#282c2b',5)+P('M781 309L856 314L863 335L773 335Z','#667c70','#3e4440',2)+E(826,284,52,12,'#9e805e','#352e30',2);
// archive
s+=R(644,365,378,91,'#59493f','#d1af7d',4);for(let i=0;i<8;i++)s+=R(660+i*44,379,30,59,i%2?'#b28a5a':'#755447','#31282c',2)+line(661+i*44,397,687+i*44,397,'#d6b57a',2);
// throne hall
s+=R(644,465,378,198,'#4a4141','#d4b47a',4);for(let i=0;i<5;i++)s+=P(`M${655+i*73} 468v189`,'none','#ab8159',6);s+=P('M782 584L780 504L858 504L858 584Z','#ad694b','#261f22',5)+R(791,545,63,43,'#d6a95d','#282329',4,8)+P('M780 506L818 480L859 505Z','#deb67a',C.ink,3)+P('M734 660L805 588L842 588L943 660Z','#6b5250','#281f23',2);
// wings barracks & quests
s+=P('M127 575L187 532L570 541L602 580Z','#704f44','#2f292a',7)+R(138,577,434,181,'#6d5d55','#2e292a',6)+R(158,595,393,142,'#3c3e3e','#c29c69',3);
for(let i=0;i<4;i++){let x=172+i*87;s+=R(x,652,72,60,'#896c5d','#d1ae80',3)+R(x+5,647,64,18,'#c3b18d','#332c2f',3)+line(x,691,x+72,691,'#332c2d',4)}s+=E(525,681,22,16,'#ba774b','#211e21',4)+P('M525 666L524 638','none','#d9b975',6);
s+=P('M1044 581L1094 533L1482 543L1520 589Z','#6e5146','#25252b',7)+R(1057,581,432,177,'#635451','#25272a',6)+R(1081,599,387,137,'#3b4443','#bb9964',3);
for(let i=0;i<5;i++){let x=1100+i*70;s+=R(x,615,55,72,'#c5aa7a','#382f2d',3,3)+line(x+8,632,x+42,630,'#53433a',2)+line(x+10,652,x+42,650,'#53433a',2)}s+=P('M1165 730L1320 689L1432 738Z','#b19269',C.ink,4);
// courtyard market gate
s+=P('M573 665L1055 665L1159 837L478 837Z','#ac8666','#332d2a',5);for(let i=0;i<6;i++)s+=P(`M${600+i*74} 746l29 91`,'none','#7d6251',2);s+=P('M482 824L632 770L705 806L660 858L455 858Z','#a3634c',C.ink,3)+P('M940 804L1002 755L1160 834L1130 858L930 858Z','#a3634c',C.ink,3);
s+=P('M563 830L612 783L663 830','#d5b281',C.ink,4)+P('M1000 830L1060 783L1115 830','#d5b281',C.ink,4);s+=P('M656 889L656 840L942 840L942 889Z','#67584c','#242328',7)+P('M760 889L760 841L840 841L840 889Z','#242328','#d4ac74',4)+R(615,821,70,62,'#80624f','#27272b',4)+R(918,821,70,62,'#80624f','#27272b',4);
// Komodo's study and yard markers
s+=R(1025,470,109,140,'#3a3a3b','#d9bb81',3)+R(1047,500,60,11,'#b99360','#262124',2)+R(1053,520,46,67,'#7f6857','#262124',2);
s+=P('M412 741Q300 780 253 830','none','#c6a57c',5)+R(254,787,86,50,'#9f7356','#2f2a2c',3);
// foreground ink details
for(let i=0;i<12;i++)s+=line(200+i*101,913,220+i*100,943,'#4d3932',3);
s+=R(24,20,1552,957,'none','#b68d58',9,14)+R(39,34,1522,925,'none','#f0d19d',2,6);
if(labelled){s+=R(460,24,680,76,'#211f25','#d5a46c',3,6)+T(800,76,'THE EMPEROR\'S FORTRESS',38,C.cream,'middle');
const labels=[[828,287,'MAP ROOM'],[830,417,'LAMPLIGHT ARCHIVE'],[821,599,'THRONE ROOM'],[360,615,'BARRACKS'],[1265,615,'QUEST ROOM'],[825,794,'MARKET COURT'],[819,926,'GATEHOUSE'],[1085,484,'KOMODO'],[280,750,'THE YARD']];for(const [x,y,t]of labels){s+=R(x-116,y-24,232,35,'#231f24','#ca9e67',1,4)+T(x,y,t,18,C.cream,'middle');}
}else{s+=R(67,56,330,45,'#28232a','#bf955e',2,5)+T(231,85,'UNLABELLED CUTAWAY',21,C.cream,'middle');}
return wrap(s);
}
// UI architectural studies
function animal(x,y,s=1,c='#262831',ears='fox'){let e=ears==='crow'?P('M-16 -83l-22 -25l27 9l23 -8l-3 20Z',c,c,3):ears==='koala'?E(-27,-77,14,16,c)+E(24,-77,14,16,c):ears==='komodo'?P('M0 -77L35 -64L25 -54L-10 -62Z',c,c,3):P('M-27 -70L-19 -107L-6 -74L17 -108L22 -72Z',c,c,3);return `<g transform="translate(${x},${y}) scale(${s})">${P('M-35 0L-23 -45L-39 -33L-33 -70L-14 -80L24 -75L35 -36L22 -48L40 0Z',c,'#161923',4)}${e}${E(0,-64,27,26,c,'#191f27',3)}${E(11,-67,2.5,2.5,'#e9b973','none',0)}${P('M-27 -29L-39 3M24 -31L38 2','none','#a47b52',3)}</g>`}
function arch(x,y,w=190,h=370){return `${R(x,y,w,h,'#252d34','#9b7a56',9)}${P(`M${x+16} ${y+h-12}L${x+16} ${y+104}Q${x+w/2} ${y-30} ${x+w-16} ${y+104}L${x+w-16} ${y+h-12}Z`,'#5d6463','#d4a86a',5)}${P(`M${x+w/2} ${y+70}V${y+h-12}M${x+17} ${y+235}H${x+w-16}`,'none','#c49a62',4)}`}
function backdrop(which){let s='';s+=R(52,166,1038,525,'url(#night)','#bb9067',4,10)+E(520,415,350,255,'url(#lamp)','none',0)+R(65,180,1008,495,'url(#grain)','none',0);
if(which==='throne'){
s+=P('M75 641L465 433L700 438L1068 652Z','#514644','#28232b',4);for(let i=0;i<5;i++){let x=92+i*208;s+=R(x,206,32,420,'#7c6154','#332d32',4)+P(`M${x-14} 214H${x+49}L${x+34} 232H${x-1}Z`,'#c09a66','#312b2b',3)}s+=arch(401,191,269,328)+P('M425 476L425 340L644 340L644 476Z','#803f3e','#33272b',4)+P('M435 345L526 292L634 345Z','#ca9b61','#33272b',4);s+=P('M475 545L477 407L591 407L591 545Z','#996944','#201f22',6)+R(483,479,101,62,'#cf9e61','#24222a',5,5)+animal(537,499,1.05,'#2d2c32','crow')+animal(830,597,1.4,'#454149','fox')+animal(281,603,1.22,'#41514d','komodo');s+=P('M76 270L243 244L243 417L76 442Z','#914f46','#cba46c',5)+P('M928 232L1063 272L1063 442L928 401Z','#914f46','#cba46c',5);
}else if(which==='quests'){
s+=R(105,205,667,389,'#705449','#cf9b64',10)+R(124,224,630,352,'#8b725c','#31282a',4);
for(let i=0;i<6;i++){let x=152+(i%3)*190,y=239+Math.floor(i/3)*157;s+=`<g transform="rotate(${(i%3-1)*6} ${x+80} ${y+60})">`+R(x,y,165,135,'#d9c5a0','#4c3831',3)+E(x+81,y+9,5,5,'#924d3f','#3b3030',2)+T(x+15,y+39,['THE FORD','MISSING','CROW DEBT','HEALER','RAID','TRUCE'][i],18,'#322a2a')+line(x+15,y+52,x+144,y+52,'#927b65',2)+line(x+15,y+71,x+131,y+71,'#927b65',2)+line(x+15,y+88,x+144,y+88,'#927b65',2)+`</g>`;}
s+=P('M795 556L1038 560L1058 642L742 643Z','#b29569','#2f2a2b',6)+P('M800 585L1043 593M827 615L1011 612','none','#5b524a',4)+animal(939,554,.9,'#3d3b3c','fox')+P('M78 658L1069 658','none','#c3a072',9);
}else if(which==='barracks'){
s+=arch(103,200,198,337)+arch(883,199,168,343);
for(let i=0;i<3;i++){let x=310+i*170;s+=R(x,332,155,184,'#514e49','#b38f63',4)+R(x+4,393,147,37,'#ccbaa0','#302b2b',4)+R(x+4,462,147,44,'#9a7666','#302b2b',4)+line(x+13,335,x+13,528,'#ac845b',5)+line(x+142,335,x+142,528,'#ac845b',5)}s+=E(183,572,75,30,'#856450','#362c2c',3)+E(183,559,34,19,'#b97943','#362c2c',3)+P('M183 545L183 505','none','#cdb68b',6)+animal(775,591,1.5,'#394647','koala')+animal(414,593,1.0,'#3e4244','crow')+P('M76 659L1068 659','none','#c3a072',9);
}else if(which==='market'){
for(let i=0;i<3;i++){let x=97+i*314;s+=R(x+22,343,280,262,'#685348','#c49b68',5)+P(`M${x-8} 355L${x+330} 355L${x+306} 262L${x+13} 262Z`,i===1?'#806e66':'#a55d49','#c8a46f',6);for(let j=0;j<5;j++)s+=P(`M${x+15+j*61} 267l10 88`,'none','#dcbf83',9);s+=R(x+31,480,255,29,'#c09c70','#352a2a',5)}
for(let i=0;i<5;i++){let x=154+i*170;s+=E(x,428,14,25,i%2?'#ceb679':'#789080','#2c2b2f',3)+line(x,399,x,349,'#ae8c61',3)}s+=animal(695,591,1.25,'#414446','fox')+animal(304,587,.91,'#4a514d','koala')+P('M74 655L1069 655','none','#c3a072',8);
}else if(which==='map'){
for(let i=0;i<5;i++){let x=80+i*204;s+=arch(x,196,165,282)}s+=P('M210 565L885 542L1028 654L105 654Z','#8a664e','#2b282c',7)+P('M241 546L866 526L951 631L175 633Z','#ccb085','#373031',4)+P('M292 563Q387 600 467 572T605 579T778 569','none','#6e8e88',22)+P('M290 580L400 551L556 608L762 570','none','#8d664b',10)+tower(526,567,.55)+bell(814,579,.53)+ridge(342,569,.39)+marsh(661,576,.35);s+=P('M570 480L738 293','none','#d1bb84',5)+E(755,278,17,17,'#e6bb73','#57443d',3)+animal(872,554,.85,'#414b4b','crow');
}else{
s+=E(580,391,295,198,'url(#lamp)','none',0)+E(585,356,115,115,'#dda366','#a17856',6)+E(628,314,107,107,'#2b3c46','none',0)+P('M120 627L432 455L783 458L1037 635Z','#76564b','#2d2829',8)+R(279,363,420,238,'#c7aa7c','#342a2a',5)+T(488,414,'CHRONICLE OF ASH',28,C.ink,'middle')+line(327,448,646,448,'#5a4639',3);for(let i=0;i<5;i++)s+=E(350+i*65,505,13,13,i===2?'#bb6653':'#d6bc84','#292526',3);s+=animal(857,568,1.25,'#353d42','komodo');}
return s}
function ui(which){const screens={throne:['THRONE ROOM','The price of the ford','Mara Reedbell asks that the old crossing be reopened.','Open a public works petition','Promise the Council nothing','Spend 36 brass on repairs'],quests:['QUEST ROOM','A road held by strangers','Two days · Eastern Ford · expires tonight','Rook + Kiyo   •   2 of 4 assigned','Chance of success 71–85%','Injury risk: 1–3 days'],barracks:['BARRACKS','Kiyo · field surgeon','Ready · The caravan has not returned.','Talk about last night','Equipment: healer’s kettle','Known: medicine, diplomacy'],market:['MARKET','The Ledger comes calling','Stock changes as the roads change.','Iron-needle kit  •  35 brass','Rain charm  •  48 brass','Infirmary treatment  •  20 brass'],map:['MAP ROOM','Kingdom ledgers','Each border is a promise made to someone.','Hollow Bell   •   Friendly','Daily taxes   •   +7 brass','Border tension   •   Rising'],chronicle:['CHRONICLE','Rewind a day, change a choice','The weather may not remember you.','Dawn 12  •  current','Dawn 11  •  available','Dawn 10  •  available']};const [title,sub,desc,a,b,c]=screens[which];let s=R(0,0,1600,900,'#111a23','none',0)+R(14,14,1572,872,'none','#a88056',5,15)+R(29,29,1542,842,'none','#68543e',2,7);
s+=R(48,47,1505,104,'#232b31','#8c6b4f',2,8)+T(75,89,'EMPEROR OF DUST',35,C.cream)+T(78,124,'ACT II  ·  DAY 17 / 50',21,C.brass);for(let i=0;i<5;i++){let x=677+i*127;s+=R(x,73,110,47,'#353a3c','#6f6054',1,5)+T(x+55,91,['LEDGER','HOUSES','YARD','WATCH','LAMPS'][i],12,C.cream,'middle')+R(x+12,101,86,7,'#3c4243','none',0,3)+R(x+12,101,30+i*11,7,i===3?'#d87b64':'#d0ab6a','none',0,3)}s+=R(1350,63,174,74,'#524333','#d1a96e',2,8)+E(1382,99,17,17,C.brass,C.ink,2)+E(1382,99,7,7,'#423b31',C.ink,2)+T(1420,109,'268',35,C.cream);
s+=backdrop(which);
s+=R(1110,166,444,525,'#2d3538','#9b7857',4,9)+R(1126,183,410,85,'#594236','#a2815e',2,4)+T(1145,218,title,26,C.cream)+T(1145,247,'ART + INTERACTION STUDY',14,C.brass);
s+=T(1145,305,sub,27,C.cream)+T(1145,335,desc,16,'#cfbaa1');s+=line(1145,358,1515,358,'#a7865a',2);
for(let i=0;i<3;i++){s+=R(1142,378+i*87,374,72,i===0?'#665544':'#394143',i===0?'#dabb83':'#6e6860',2,7)+T(1160,407+i*87,[a,b,c][i],18,C.cream)+T(1160,430+i*87,i===0?'● SELECTED':'○ AVAILABLE',13,i===0?'#f6d69b':'#b4b3aa');}
s+=R(52,713,1502,135,'#232c34','#95714d',3,9)+T(82,753,which==='throne'?'AUDIENCE 01 / 03':which==='quests'?'DISPATCH BOARD':which==='barracks'?'FOLLOWER PROFILE':which==='market'?'TRADERS IN THE OUTER COURT':which==='map'?'THE KINGDOM REMEMBERS':'TIMELINE AND DAWN REPORT',21,C.brass);
s+=T(83,788,which==='throne'?'“If the crossing breaks, my town starves before your taxes arrive.”':which==='quests'?'Choose 1–4 followers, review the odds, then send them into the wasteland.':which==='barracks'?'Portraits, injuries, equipment and conversation occupy one illustrated stage.':which==='market'?'Turn brass into tools, treatments and hard bargains.':which==='map'?'Borders and faction banners are overlays on the illustrated base map.':'Save, load and rewind. A second chance never guarantees the same event.',20,C.cream);
s+=R(1286,765,234,54,'#b78654','#362e2d',3,6)+T(1404,801,which==='chronicle'?'REWIND':'FINISH DAY',22,'#211e22','middle');
s+=R(78,174,217,32,'#28272d','#cba069',1,3)+T(187,196,'CONCEPT STUDY',16,C.cream,'middle');return wrap(s,1600,900)}
const assets={
'wasteland-base.svg':mapBase(false),
'wasteland-reference.svg':mapBase(true),
'wasteland-day41-overlay.svg':mapBase(false,true),
'fortress-cutaway-base.svg':fortress(false),
'fortress-cutaway-reference.svg':fortress(true),
...Object.fromEntries(['throne','quests','barracks','market','map','chronicle'].map(n=>[`screen-${n}.svg`,ui(n)]))};
if(require.main===module){fs.mkdirSync(OUTPUT,{recursive:true});for(const [n,v] of Object.entries(assets))fs.writeFileSync(path.join(OUTPUT,n),v);console.log(Object.keys(assets).map(x=>x+' '+assets[x].length).join('\n'));}
module.exports={assets,mapBase,fortress,ui};
