import tkinter as tk
from tkinter import Label, Scrollbar, ttk, filedialog, messagebox, colorchooser, simpledialog, Button, Canvas
import json, os
from datetime import datetime
from PIL import Image, ImageTk, ImageOps,ImageChops
from dataclasses import dataclass
import subprocess
import bisect
import re,ast
import webbrowser
import random
from functools import partial

@dataclass
class Item:
    english: str
    id:      int
sd_items = {
 "보석 카테고리": Item(english="category_gem", id=-2),
 "생선 카테고리": Item(english="category_fish", id=-4),
 "달걀 카테고리": Item(english="category_egg", id=-5),
 "우유 카테고리": Item(english="category_milk", id=-6),
"요리 카테고리": Item(english="category_cooking", id=-7),
"광물 카테고리": Item(english="category_ｍinerals", id=-12),
"쓰레기 카테고리": Item(english="category_junk", id=-20),
"장인 카테고리": Item(english="category_artisan_goods", id=-26),
"시럽 카테고리": Item(english="category_syrup", id=-27),
"채소 카테고리": Item(english="category_vegetable", id=-75),
"꽃 카테고리": Item(english="category_flowers", id=-80),
"과일 카테고리": Item(english="category_fruits", id=-79),
"채집 카테고리": Item(english="category_greens", id=-81),
"야생 고추냉이" : Item(english="WildHorseradish", id=16),
"수선화" : Item(english="Daffodil", id=18),
"리크" : Item(english="Leek", id=20),
"민들레" : Item(english="Dandelion", id=22),
"파스닙" : Item(english="Parsnip", id=24),
"목재" : Item(english="Lumber", id=30),
"에메랄드" : Item(english="Emerald", id=60),
"아쿠아마린" : Item(english="Aquamarine", id=62),
"루비" : Item(english="Ruby", id=64),
"자수정" : Item(english="Amethyst", id=66),
"토파즈" : Item(english="Topaz", id=68),
"제이드" : Item(english="Jade", id=70),
"다이아몬드" : Item(english="Diamond", id=72),
"무지개빛 파편" : Item(english="Prismatic Shard", id=74),
"동굴 당근" : Item(english="Cave Carrot", id=78),
"석영" : Item(english="Quartz", id=80),
"불석영" : Item(english="Fire Quartz", id=82),
"얼어붙은 눈물" : Item(english="Frozen Tear", id=84),
"대지의 수정" : Item(english="Earth Crystal", id=86),
"코코넛" : Item(english="Coconut", id=88),
"선인장 열매" : Item(english="Cactus Fruit", id=90),
"수액" : Item(english="Sap", id=92),
"드워프 두루마리 1" : Item(english="Dwarf Scroll 1", id=96),
"드워프 두루마리 2" : Item(english="Dwarf Scroll 2", id=97),
"드워프 두루마리 3" : Item(english="Dwarf Scroll 3", id=98),
"드워프 두루마리 4" : Item(english="Dwarf Scroll 4", id=99),
"깨진 암포라" : Item(english="Chipped Amphora", id=100),
"화살촉" : Item(english="Arrowhead", id=101),
"고대 인형" : Item(english="Ancient Doll", id=103),
"엘프 장신구" : Item(english="Evlish Jewelry", id=104),
"씹는 막대" : Item(english="Chewing Stick", id=105),
"화려한 부채" : Item(english="Ornamental Fan", id=106),
"공룡알" : Item(english="Dinosaur Egg", id=107),
"희귀한 원반" : Item(english="Rare Disc", id=108),
"고대 검" : Item(english="Ancient Sword", id=109),
"녹슨 숟가락" : Item(english="Rusty Spoon", id=110),
"녹슨 징" : Item(english="Rusty Spur", id=111),
"녹슨 톱니바퀴" : Item(english="Rusty Cog", id=112),
"닭 조각상" : Item(english="Chicken Statue", id=113),
"고대 씨앗" : Item(english="Ancient Seed", id=114),
"선사 시대 도구" : Item(english="Prehistoric Tool", id=115),
"말린 불가사리" : Item(english="Dried Starfish", id=116),
"닻" : Item(english="Anchor", id=117),
"유리 파편" : Item(english="Glass Shards", id=118),
"뼈 피리" : Item(english="Bone Flute", id=119),
"선사 시대 손도끼" : Item(english="Prehistoric Handaxe", id=120),
"드워프 헬멧" : Item(english="Dwarvish Helm", id=121),
"드워프 도구" : Item(english="Dwarf Gadget", id=122),
"고대 북" : Item(english="Ancient Drum", id=123),
"황금 가면" : Item(english="Golden Mask", id=124),
"황금 유물" : Item(english="Golden Relic", id=125),
"이상한 인형 초록" : Item(english="Strange Doll A", id=126),
"이상한 인형 핑크" : Item(english="Strange Doll B", id=127),
"복어" : Item(english="Pufferfish", id=128),
"멸치" : Item(english="Anchovy", id=129),
"참치" : Item(english="Tuna", id=130),
"정어리" : Item(english="Sardine", id=131),
"도미" : Item(english="Bream", id=132),
"큰입배스" : Item(english="Largemouth Bass", id=136),
"작은입배스" : Item(english="SmallmouthBass", id=137),
"무지개송어" : Item(english="Rainbow Trout", id=138),
"연어" : Item(english="Salmon", id=139),
"월아이" : Item(english="Walleye", id=140),
"농어" : Item(english="Perch", id=141),
"잉어" : Item(english="Carp", id=142),
"메기" : Item(english="Catfish", id=143),
"파이크" : Item(english="Pike", id=144),
"개복치" : Item(english="Sunfish", id=145),
"붉은숭어" : Item(english="Red Mullet", id=146),
"청어" : Item(english="Herring", id=147),
"장어" : Item(english="Eel", id=148),
"문어" : Item(english="Octopus", id=149),
"붉은도미" : Item(english="Red Snapper", id=150),
"오징어" : Item(english="Squid", id=151),
"해초" : Item(english="Seaweed", id=152),
"녹조류" : Item(english="Green Algae", id=153),
"해삼" : Item(english="Sea Cucumber", id=154),
"슈퍼오이" : Item(english="Super Cucumber", id=155),
"귀신고기" : Item(english="Ghostfish", id=156),
"흰조류" : Item(english="White Algae", id=157),
"스톤피쉬" : Item(english="Stonefish", id=158),
"크림슨피쉬" : Item(english="Crimsonfish", id=159),
"앵글러" : Item(english="Angler", id=160),
"아이스핍" : Item(english="Ice Pip", id=161),
"용암장어" : Item(english="Lava Eel", id=162),
"전설" : Item(english="Legend", id=163),
"도루묵" : Item(english="Sandfish", id=164),
"전갈잉어" : Item(english="Scorpion Carp", id=165),
"조자콜라" : Item(english="Joja Cola", id=167),
"쓰레기" : Item(english="Trash", id=168),
"유목" : Item(english="Driftwood", id=169),
"깨진 유리잔" : Item(english="Broken Glasses", id=170),
"깨진 CD" : Item(english="Broken CD", id=171),
"젖은 신문지" : Item(english="Soggy Newspaper", id=172),
"큰 흰 달걀" : Item(english="Large White Egg", id=174),
"흰 달걀" : Item(english="White Egg", id=176),
"갈색 달걀" : Item(english="Brown Egg", id=180),
"큰 갈색 달걀" : Item(english="Large Brown Egg", id=182),
"우유" : Item(english="Milk", id=184),
"큰 우유" : Item(english="Large Milk", id=186),
"그린빈" : Item(english="Green Bean", id=188),
"콜리플라워" : Item(english="Cauliflower", id=190),
"감자" : Item(english="Potato", id=192),
"계란 프라이" : Item(english="Fried Egg", id=194),
"오믈렛" : Item(english="Omelet", id=195),
"샐러드" : Item(english="Salad", id=196),
"치즈 콜리플라워" : Item(english="Cheese Cauliflower", id=197),
"구운 생선" : Item(english="Baked Fish", id=198),
"파스닙 수프" : Item(english="Parsnip Soup", id=199),
"야채 모듬" : Item(english="Vegetable Medley", id=200),
"완벽한 아침 식사" : Item(english="Complete Breakfast", id=201),
"오징어 튀김" : Item(english="Fried Calamari", id=202),
"이상한 빵" : Item(english="Strange Bun", id=203),
"럭키 런치" : Item(english="Lucky Lunch", id=204),
"버섯 튀김" : Item(english="Fried Mushroom", id=205),
"피자" : Item(english="Pizza", id=206),
"콩 핫팟" : Item(english="Bean Hotpot", id=207),
"글레이즈드 얌" : Item(english="Glazed Yams", id=208),
"잉어 서프라이즈" : Item(english="Carp Suprise", id=209),
"해시브라운" : Item(english="Hashbrowns", id=210),
"팬케이크" : Item(english="Pancakes", id=211),
"연어 저녁 식사" : Item(english="Salmon Dinner", id=212),
"피시 타코" : Item(english="FishTaco", id=213),
"바삭한 농어" : Item(english="Crispy Bass", id=214),
"페퍼 포퍼" : Item(english="Pepper Poppers", id=215),
"빵" : Item(english="Bread", id=216),
"톰 카 수프" : Item(english="Tom Kha Soup", id=218),
"송어 수프" : Item(english="Trout Soup", id=219),
"초콜릿 케이크" : Item(english="Chocolate Cake", id=220),
"핑크 케이크" : Item(english="Pink Cake", id=221),
"루바브 파이" : Item(english="Rhubarb Pie", id=222),
"쿠키" : Item(english="Cookie", id=223),
"스파게티" : Item(english="Spaghetti", id=224),
"장어 튀김" : Item(english="Fried Eel", id=225),
"매콤한 장어" : Item(english="Spicy Eel", id=226),
"사시미" : Item(english="Sashimi", id=227),
"마키 롤" : Item(english="Maki Roll", id=228),
"또띠아" : Item(english="Tortilla", id=229),
"레드 플레이트" : Item(english="Red Plate", id=230),
"가지 파마산" : Item(english="Eggplant Parmesan", id=231),
"라이스 푸딩" : Item(english="Rice Pudding", id=232),
"아이스크림" : Item(english="Ice Cream", id=233),
"블루베리 타르트" : Item(english="Blueberry Tart", id=234),
"가을의 수확" : Item(english="Autumn's Bounty", id=235),
"호박 수프" : Item(english="Pumpkin Soup", id=236),
"슈퍼 밀" : Item(english="Super Meal", id=237),
"크랜베리 소스" : Item(english="Cranberry Sauce", id=238),
"스터핑" : Item(english="Stuffing", id=239),
"파머스 런치" : Item(english="Farmer's Lunch", id=240),
"서바이벌 버거" : Item(english="Survival Burger", id=241),
"바다 요리" : Item(english="Dish O' The Sea", id=242),
"광부의 간식" : Item(english="Miner's Treat", id=243),
"뿌리 플래터" : Item(english="Roots Platter", id=244),
"식용유" : Item(english="Cooking Oil", id=247),
"마늘" : Item(english="Garlic", id=248),
"케일" : Item(english="Kale", id=250),
"루바브" : Item(english="Rhubarb", id=252),
"트리플 샷 에스프레소" : Item(english="Triple Shot Espresso", id=253),
"멜론" : Item(english="Melon", id=254),
"토마토" : Item(english="Tomato", id=256),
"모렐 버섯" : Item(english="Morel", id=257),
"블루베리" : Item(english="Blueberry", id=258),
"고사리" : Item(english="Fiddlehead Fern", id=259),
"매운 고추" : Item(english="Hot Pepper", id=260),
"밀" : Item(english="Wheat", id=262),
"무" : Item(english="Radish", id=264),
"바다거품 푸딩" : Item(english="Seafoam Pudding", id=265),
"적양배추" : Item(english="Red Cabbage", id=266),
"넙치" : Item(english="Flounder", id=267),
"스타프루트" : Item(english="Starfruit", id=268),
"미드나잇 잉어" : Item(english="Midnight Carp", id=269),
"옥수수" : Item(english="Corn", id=270),
"정제되지 않은 쌀" : Item(english="Unmilled Rice", id=271),
"가지" : Item(english="Eggplant", id=272),
"아티초크" : Item(english="Artichoke", id=274),
"호박" : Item(english="Pumpkin", id=276),
"청경채" : Item(english="Bok Choy", id=278),
"매직 락 캔디" : Item(english="Magic Rock Candy", id=279),
"얌" : Item(english="Yam", id=280),
"살구버섯" : Item(english="Chanterelle", id=281),
"크랜베리" : Item(english="Cranberries", id=282),
"홀리" : Item(english="Holly", id=283),
"비트" : Item(english="Beet", id=284),
"살몬베리" : Item(english="Salmonberry", id=296),
"아마란스" : Item(english="Amaranth", id=300),
"페일 에일" : Item(english="Pale Ale", id=303),
"홉" : Item(english="Hops", id=304),
"보이드 에그" : Item(english="Void Egg", id=305),
"마요네즈" : Item(english="Mayonnaise", id=306),
"오리 마요네즈" : Item(english="Duck Mayonnaise", id=307),
"보이드 마요네즈" : Item(english="Void Mayonnaise", id=308),
"구리 막대" : Item(english="Copper Bar", id=334),
"철 막대" : Item(english="Iron Bar", id=335),
"금 막대" : Item(english="Gold Bar", id=336),
"이리듐 막대" : Item(english="Iridium Bar", id=337),
"정제 석영" : Item(english="Refined Quartz", id=338),
"꿀" : Item(english="Honey", id=340),
"피클" : Item(english="Pickles", id=342),
"젤리" : Item(english="Jelly", id=344),
"맥주" : Item(english="Beer", id=346),
"와인" : Item(english="Wine", id=348),
"에너지 토닉" : Item(english="Energy Tonic", id=349),
"주스" : Item(english="Juice", id=350),
"조개" : Item(english="Clam", id=372),
"황금 호박" : Item(english="Golden Pumpkin", id=373),
"양귀비" : Item(english="Poppy", id=376),
"앵무조개 껍데기" : Item(english="Nautilus Shell", id=392),
"산호" : Item(english="Coral", id=393),
"무지개 껍데기" : Item(english="Rainbow Shell", id=394),
"커피" : Item(english="Coffee", id=395),
"스파이스 베리" : Item(english="Spice Berry", id=396),
"성게" : Item(english="Sea Urchin", id=397),
"포도" : Item(english="Grape", id=398),
"파" : Item(english="Spring Onion", id=399),
"딸기" : Item(english="Strawberry", id=400),
"스위트피" : Item(english="Sweet Pea", id=402),
"들판 간식" : Item(english="Field Snack", id=403),
"버섯" : Item(english="Common Mushroom", id=404),
"야생 자두" : Item(english="Wild Plum", id=406),
"헤이즐넛" : Item(english="Hazelnut", id=408),
"블랙베리" : Item(english="Blackberry", id=410),
"겨울 뿌리" : Item(english="Winter Root", id=412),
"크리스털 과일" : Item(english="Crystal Fruit", id=414),
"설탕 얌" : Item(english="Snow Yam", id=416),
"스위트 젬 베리" : Item(english="Sweet Gem Berry", id=417),
"크로커스" : Item(english="Crocus", id=418),
"붉은 버섯" : Item(english="Red Mushroom", id=420),
"해바라기" : Item(english="Sunflower", id=421),
"자색 버섯" : Item(english="Purple Mushroom", id=422),
"쌀" : Item(english="Rice", id=423),
"치즈" : Item(english="Cheese", id=424),
"염소 치즈" : Item(english="Goat Cheese", id=312),
"천" : Item(english="Cloth", id=428),
"트러플" : Item(english="Truffle", id=430),
"트러플 오일" : Item(english="Truffle Oil", id=432),
"커피콩" : Item(english="Coffee Bean", id=433),
"염소 우유" : Item(english="Goat Milk", id=436),
"큰 염소 우유" : Item(english="Large Goat Milk", id=48),
"양털" : Item(english="Wool", id=440),
"오리알" : Item(english="Duck Egg", id=442),
"오리 깃털" : Item(english="Duck Feather", id=444),
"캐비어" : Item(english="Caviar", id=445),
"토끼 발" : Item(english="Rabbit's Foot", id=446),
"숙성된 어란" : Item(english="Aged Roe", id=447),
"고대 과일" : Item(english="Ancient Fruit", id=454),
"해조류 수프" : Item(english="Algae Soup", id=456),
"페일 브로스" : Item(english="Pale Broth", id=457),
"미드" : Item(english="Mead", id=459),
"알라마이트" : Item(english="Alamite", id=538),
"빅사이트" : Item(english="Bixite", id=539),
"중정석" : Item(english="Baryte", id=540),
"에어리나이트" : Item(english="Aerinite", id=541),
"방해석" : Item(english="Calcite", id=542),
"돌로마이트" : Item(english="Dolomite", id=543),
"에스페라이트" : Item(english="Esperite", id=544),
"플루오르인회석" : Item(english="Fluorapatite", id=545),
"제미나이트" : Item(english="Geminite", id=546),
"헬바이트" : Item(english="Helvite", id=547),
"잠보라이트" : Item(english="Jamborite", id=548),
"재고아이트" : Item(english="Jagoite", id=549),
"카이야나이트" : Item(english="Kyanite", id=550),
"루나라이트" : Item(english="Lunarite", id=551),
"공작석" : Item(english="Malachite", id=552),
"넵투나이트" : Item(english="Neptunite", id=553),
"레몬 스톤" : Item(english="Lemon Stone", id=554),
"네코아이트" : Item(english="Nekoite", id=555),
"오피먼트" : Item(english="Orpiment", id=556),
"석화된 슬라임" : Item(english="Petrified Slime", id=557),
"썬더 에그" : Item(english="Thunder Egg", id=558),
"황철석" : Item(english="Pyrite", id=559),
"오션 스톤" : Item(english="Ocean Stone", id=560),
"고스트 크리스털" : Item(english="Ghost Crystal", id=561),
"타이거아이" : Item(english="Tigerseye", id=562),
"벽옥" : Item(english="Jasper", id=563),
"오팔" : Item(english="Opal", id=564),
"파이어 오팔" : Item(english="Fire Opal", id=565),
"셀레스틴" : Item(english="Celestine", id=566),
"대리석" : Item(english="Marble", id=567),
"사암" : Item(english="Sandstone", id=568),
"화강암" : Item(english="Granite", id=569),
"현무암" : Item(english="Basalt", id=570),
"석회암" : Item(english="Limestone", id=571),
"동석" : Item(english="Soapstone", id=572),
"적철석" : Item(english="Hematite", id=573),
"이암" : Item(english="Mudstone", id=574),
"흑요석" : Item(english="Obsidian", id=575),
"슬레이트" : Item(english="Slate", id=576),
"요정석" : Item(english="Fairy Stone", id=577),
"별 조각" : Item(english="Star Shards", id=578),
"선사 시대 견갑골" : Item(english="Prehistoric Scapula", id=579),
"골격 꼬리" : Item(english="Skeletal Tail", id=585),
"앵무조개 화석" : Item(english="Nautilus Fossil", id=586),
"양서류 화석" : Item(english="Amphibian Fossil", id=587),
"야자수 화석" : Item(english="Palm Fossil", id=588),
"삼엽충" : Item(english="Trilobite", id=589),
"튤립" : Item(english="Tulip", id=591),
"썸머 스팽글" : Item(english="Summer Spangle", id=593),
"요정 장미" : Item(english="Fairy Rose", id=595),
"블루 재즈" : Item(english="Blue Jazz", id=597),
"플럼 푸딩" : Item(english="Plum Pudding", id=604),
"아티초크 딥" : Item(english="Artichoke Dip", id=605),
"볶음 요리" : Item(english="Stir Fry", id=606),
"구운 헤이즐넛" : Item(english="Roasted Hazelnuts", id=607),
"호박 파이" : Item(english="Pumpkin Pie", id=608),
"무 샐러드" : Item(english="Radish Salad", id=609),
"과일 샐러드" : Item(english="Fruit Salad", id=610),
"블랙베리 코블러" : Item(english="Blackberry Cobbler", id=611),
"크랜베리 캔디" : Item(english="Cranberry Candy", id=612),
"사과" : Item(english="Apple", id=613),
"녹차" : Item(english="Green Tea", id=614),
"브루스케타" : Item(english="Bruschetta", id=618),
"살구" : Item(english="Apricot", id=634),
"오렌지" : Item(english="Orange", id=635),
"복숭아" : Item(english="Peach", id=636),
"석류" : Item(english="Pomegranate", id=637),
"체리" : Item(english="Cherry", id=638),
"코울슬로" : Item(english="Coleslaw", id=648),
"고사리 리조또" : Item(english="Fiddlehead Risotto", id=649),
"양귀비씨 머핀" : Item(english="Poppyseed Muffin", id=651),
"돌연변이 잉어" : Item(english="Mutant Carp", id=682),
"벌레 고기" : Item(english="Bug Meat", id=684),
"미끼" : Item(english="Bait", id=685),
"철갑상어" : Item(english="Sturgeon", id=698),
"타이거 트라우트" : Item(english="Tiger Trout", id=699),
"불헤드" : Item(english="Bullhead", id=700),
"틸라피아" : Item(english="Tilapia", id=701),
"처브" : Item(english="Chub", id=702),
"도라도" : Item(english="Dorado", id=704),
"날개다랑어" : Item(english="Albacore", id=705),
"전어" : Item(english="Shad", id=706),
"링코드" : Item(english="Lingcod", id=707),
"넙치" : Item(english="Halibut", id=708),
"랍스터" : Item(english="Lobster", id=715),
"가재" : Item(english="Crayfish", id=716),
"게" : Item(english="Crab", id=717),
"꼬막" : Item(english="Cockle", id=718),
"홍합" : Item(english="Mussel", id=719),
"새우" : Item(english="Shrimp", id=720),
"달팽이" : Item(english="Snail", id=721),
"빈카" : Item(english="Periwinkle", id=722),
"굴" : Item(english="Oyster", id=723),
"메이플 시럽" : Item(english="Maple Syrup", id=724),
"참나무 수지" : Item(english="Oak Resin", id=725),
"소나무 타르" : Item(english="Pine Tar", id=726),
"차우더" : Item(english="Chowder", id=727),
"생선 스튜" : Item(english="Fish Stew", id=728),
"에스카르고" : Item(english="Escargot", id=729),
"랍스터 비스크" : Item(english="Lobster Bisque", id=730),
"메이플 바" : Item(english="Maple Bar", id=731),
"크랩 케이크" : Item(english="Crab Cakes", id=732),
"새우 칵테일" : Item(english="Shrimp Cocktail", id=733),
"우드스킵" : Item(english="Woodskip", id=734),
"더러운 것" : Item(english="Slime", id=766),
"배트 윙" : Item(english="Bat Wing", id=767),
"태양의 정수" : Item(english="Solar Essence", id=768),
"공허 정수" : Item(english="Void Essence", id=769),
"마늘 오일" : Item(english="Oil of Garlic", id=772),
"생명의 비약" : Item(english="Life Elixir", id=773),
"야생 미끼" : Item(english="Wild Bait", id=774),
"빙하고기" : Item(english="Glacierfish", id=775),
"배터리 팩" : Item(english="Battery Pack", id=787),
"공허의 연어" : Item(english="Void Salmon", id=795),
"슬라임잭" : Item(english="Slimejack", id=796),
"진주" : Item(english="Pearl", id=797),
"자정 오징어" : Item(english="Midnight Squid", id=798),
"유령 물고기" : Item(english="Spook Fish", id=799),
"블롭피쉬" : Item(english="Blobfish", id=800),
"공룡 마요네즈" : Item(english="Dinosaur Mayonnaise", id=807),
"어란" : Item(english="Roe", id=812),
"오징어 먹물" : Item(english="Squid Ink", id=814),
"찻잎" : Item(english="Tea Leaves", id=815),
             } #key:한글이름, v.english:영어이름 v.id:아이템코드
Object={k:v.id for k,v in sd_items.items() if v.id>0}
location_name=["Farm","AbandonedJojaMart","AnimalShop","ArchaeologyHouse",
               "Backwoods","BathHouse_Pool","Beach","BoatTunnel",
               "BusStop","CommunityCenter","DesertFestival",
               "ElliottHouse","FarmHouse","FishShop",
               "Forest","HaleyHouse","HarveyRoom","Hospital",
               "IslandHut","IslandNorth","IslandSouth","IslandWest",
               "JoshHouse","LeahHouse","ManorHouse","Mine","Mountain",
               "QiNutRoom","Railroad","Saloon","SamHouse","SandyHouse",
               "ScienceHouse","SebastianRoom","SeedShop","Sewer","Sunroom",
               "Temp","Tent","Town","Trailer","Trailer_Big","WizardHouse","Woods"]
CraftingRecepies={"나무 울타리":"Wood Fence","돌 울타리":"Stone Fence","철 울타리":"Iron Fence","나무 울타리":"Hardwood Fence","잔디 발아기":"Grass Starter",
    "대문":"Gate","상자":"Chest","횃불":"Torch","허수아비":"Scarecrow","고급 허수아비":"Deluxe Scarecrow",
    "벌집":"Bee House","술통":"Keg","통":"Cask","용광로":"Furnace","화분":"Garden Pot",
    "나무 간판":"Wood Sign","돌 간판":"Stone Sign","치즈 프레스":"Cheese Press","마요네즈 제조기":"Mayonnaise Machine","씨앗 제조기":"Seed Maker",
    "베틀":"Loom","기름 제조기":"Oil Maker","재활용 기계":"Recycling Machine","벌레통":"Worm Bin","보존 용기":"Preserves Jar",
    "숯 가마":"Charcoal Kiln","수액 채취기":"Tapper","피뢰침":"Lightning Rod","슬라임 부화기":"Slime Incubator","슬라임 달걀 압착기":"Slime Egg-Press",
    "수정관":"Crystalarium","미니 주크박스":"Mini-Jukebox","스프링클러":"Sprinkler","고급 스프링클러":"Quality Sprinkler","이리듐 스프링클러":"Iridium Sprinkler",
    "계단":"Staircase","플루트 블록":"Flute Block","드럼 블록":"Drum Block","기본 비료":"Basic Fertilizer","나무 비료":"Tree Fertilizer",
    "고급 비료":"Quality Fertilizer","기본 유지 토양":"Basic Retaining Soil","고급 유지 토양":"Quality Retaining Soil","스피드 그로":"Speed-Gro","고급 스피드 그로":"Deluxe Speed-Gro",
    "하이퍼 스피드 그로":"Hyper Speed-Gro","고급 비료":"Deluxe Fertilizer","고급 유지 토양":"Deluxe Retaining Soil","체리 폭탄":"Cherry Bomb","폭탄":"Bomb",
    "메가 폭탄":"Mega Bomb","폭발성 탄약":"Explosive Ammo","변환(철)":"Transmute (Fe)","변환 (Au)":"Transmute (Au)","고대 씨앗":"Ancient Seeds",
    "야생 씨앗 (Sp)":"Wild Seeds (Sp)","야생 씨앗 (Su)":"Wild Seeds (Su)","야생 씨앗 (Fa)":"Wild Seeds (Fa)","야생 씨앗 (Wi)":"Wild Seeds (Wi)","섬유 씨앗":"Fiber Seeds",
    "차나무 묘목":"Tea Sapling","워프 토템: 농장":"Warp Totem: Farm","워프 토템: 산":"Warp Totem: Mountains","워프 토템: 해변":"Warp Totem: Beach","워프 토템: 사막":"Warp Totem: Desert",
    "워프 토템: 섬":"Warp Totem: Island","비 토템":"Rain Totem","야외용 키트":"Cookout Kit","야외 간식":"Field Snack","잭오랜턴":"Jack-O-Lantern",
    "나무 바닥":"Wood Floor","짚 바닥":"Straw Floor","풍화된 바닥":"Weathered Floor","소박한 판자 바닥":"Rustic Plank Floor","수정 바닥":"Crystal Floor",
    "돌 바닥":"Stone Floor","돌 보도 바닥":"Stone Walkway Floor","벽돌 바닥":"Brick Floor","나무 길":"Wood Path","자갈길":"Gravel Path",
    "조약돌 길":"Cobblestone Path","디딤돌 길":"Stepping Stone Path","수정 길":"Crystal Path","야생 미끼":"Wild Bait","미끼":"Bait",
    "스피너":"Spinner","자석":"Magnet","덫 찌개":"Trap Bobber","코르크 찌개":"Cork Bobber","드레싱 스피너":"Dressed Spinner",
    "보물 사냥꾼":"Treasure Hunter","가시 돋친 갈고리":"Barbed Hook","마늘 기름":"Oil Of Garlic","생명의 영약":"Life Elixir","게 통":"Crab Pot",
    "이리듐 밴드":"Iridium Band","결혼 반지":"Wedding Ring","요바 반지":"Ring of Yoba","튼튼한 반지":"Sturdy Ring","전사 반지":"Warrior Ring",
    "꽃통":"Tub o' Flowers","나무 화로":"Wooden Brazier","사악한 조각상":"Wicked Statue","돌 화로":"Stone Brazier","금 화로":"Gold Brazier",
    "캠프파이어":"Campfire","그루터기 화로":"Stump Brazier","조각 화로":"Carved Brazier","해골 화로":"Skull Brazier","통 화로":"Barrel Brazier",
    "대리석 화로":"Marble Brazier","나무 가로등":"Wood Lamp-post","철 가로등":"Iron Lamp-post","요정 가루":"Fairy Dust","벌레 스테이크":"Bug Steak",
    "어둠의 표지판":"Dark Sign","고급 밥버":"Quality Bobber","돌 상자":"Stone Chest","몬스터 머스크":"Monster Musk","미니 오벨리스크":"Mini-Obelisk",
    "농장용 컴퓨터":"Farm Computer","타조 부화기":"Ostrich Incubator","정동석 분쇄기":"Geode Crusher","태양광 패널":"Solar Panel","뼈 분쇄기":"Bone Mill",
    "가시 고리":"Thorns Ring","발광석 고리":"Glowstone Ring","헤비 탭퍼":"Heavy Tapper","호퍼":"Hopper","매직 베이트":"Magic Bait"}
CookingRecepies={"계란 프라이":"Fried Egg","오믈렛":"Omelet","샐러드":"Salad","치즈 콜리플라워":"Cheese Cauliflower","구운 생선":"Baked Fish",
    "파스닙 수프":"Parsnip Soup","야채 모듬":"Vegetable Medley","완벽한 아침 식사":"Complete Breakfast","오징어 튀김":"Fried Calamari","이상한 빵":"Strange Bun",
    "행운의 점심":"Lucky Lunch","버섯 튀김":"Fried Mushroom","피자":"Pizza","콩":"Bean","핫팟":"Hotpot",
    "글레이즈드 얌":"Glazed Yams","잉어 서프라이즈":"Carp Surprise","해시브라운":"Hashbrowns","팬케이크":"Pancakes","연어 저녁 식사":"Salmon Dinner",
    "피시 타코":"Fish Taco","바삭한 농어":"Crispy Bass","페퍼 포퍼":"Pepper Poppers","빵":"Bread","톰 카 수프":"Tom Kha Soup",
    "송어 수프":"Trout Soup","초콜릿 케이크":"Chocolate Cake","핑크 케이크":"Pink Cake","루바브 파이":"Rhubarb Pie","쿠키":"Cookie",
    "스파게티":"Spaghetti","장어 튀김":"Fried Eel","매콤한 장어":"Spicy Eel","사시미":"Sashimi","마키 롤":"Maki Roll",
    "또띠아":"Tortilla","레드 플레이트":"Red Plate","가지 파마산":"Eggplant Parmesan","라이스 푸딩":"Rice Pudding","아이스크림":"Ice Cream",
    "블루베리 타르트":"Blueberry Tart","가을의 풍요로움":"Autumn's Bounty","호박 수프":"Pumpkin Soup","슈퍼 밀":"Super Meal","크랜베리 소스":"Cranberry Sauce",
    "농부의 점심":"Farmer's Lunch","생존 버거":"Survival Burger","바다 요리":"Dish o' The Sea","광부의 간식":"Miner's Treat","루츠 플래터":"Roots Platter",
    "트리플 샷 에스프레소":"Triple Shot Espresso","씨폼 푸딩":"Seafoam Pudding","해조류 수프":"Algae Soup","페일 브로스":"Pale Broth","플럼 푸딩":"Plum Pudding",
    "아티초크 딥":"Artichoke Dip","볶음 요리":"Stir Fry","구운 헤이즐넛":"Roasted Hazelnuts","호박 파이":"Pumpkin Pie","무 샐러드":"Radish Salad",
    "과일 샐러드":"Fruit Salad","블랙베리 코블러":"Blackberry Cobbler","크랜베리 캔디":"Cranberry Candy","브루스케타":"Bruschetta","코울슬로":"Coleslaw",
    "피들헤드 리조또":"Fiddlehead Risotto","양귀비씨 머핀":"Poppyseed Muffin","차우더":"Chowder","생선 스튜":"Fish Stew","에스카르고":"Escargot",
    "랍스터 비스크":"Lobster Bisque","메이플 바":"Maple Bar","크랩 케이크":"Crab Cakes","새우 칵테일":"Shrimp Cocktail","진저에일":"Ginger Ale",
    "바나나 푸딩":"Banana Pudding","망고 스티키 라이스":"Mango Sticky Rice","포이":"Poi","트로피컬 카레":"Tropical Curry","오징어 먹물 라비올리":"Squid Ink Ravioli"
}
DayOfWeek={"월":"Mon","화":"The","수":"Wed","목":"Thu","금":"Fri","토":"Sat","일":"Sun"}
Season={"봄":"spring","여름":"summer","가을":"fall","겨울":"winter"}
Weather={"해":"sunny","비":"rainy","녹색 비":"green rain","바람":"debris","폭풍":"stormy","축제":"festival","눈":"snowy","웨딩":"wedding"}
NPCName=["Abigail","Alex","Caroline","Clint","Demetrius","Dwarf","Emily","Elliott","Evelyn","George","Gus","Haley","Harvey","Jas","Jodi","Kent","Krobus","Leo","Leah","Lewis","Linus","Marnie","Maru","Pam","Penny","Robin","Sam","Sebastian","Shane","Sandy","Vincent","Wizard"]
FNPCName=NPCName+["farmer"]
Building={"주니모 오두막":"Junimo_Hut","골드 시계":"Gold_Clock","닭장":"Coop","헛간":"Barn",
                        "우물":"Well","저장고":"Silo","제분기":"Mill","헛간":"Shed",
                        "물고기 연못":"Fish_Pond","오두막":"Cabin","반려동물 그릇":"Pet_Bowl","마구간":"Stable","슬라임장":"Slime_Hutch",
                        "배송 상자":"Shipping_Bin","농장":"Farmhouse","온실":"Greenhouse"}
user_question={}
user_event={}

Skill={"전투":"Combat", "농사":"Farming", "낚시":"Fishing", "채집":"Foraging", "행운":"Luck", "채광":"Mining"}
Direction={"위":"0","오른쪽":"1","아래":"2","왼쪽":"3"};BoolLoop={"한 번":"false","계속":"true"}
Actor=["robot","Bear","SeaMonsterKrobus","Grandpa","Marcello"]+NPCName
Awardable=["rod","pot","sculpture","slimeEgg","jukebox","(T)TrainingRod","emilyClothes","samBoombox","marniePainting","sword","Pan","hero","joja","rod","pot"]
Emote={"💧?":"4","?":"8",";;;":"12","!":"16","❤️":"20","💤":"24","💧":"28","^ㅅ^":"32","✖️":"36","•••":"40","unused":"44","🌼":"48","🎮 ":"52","🎵 ":"56","///":"60"}
FarmerEye={"열림":0, "감김":1, "오른쪽":2, "왼쪽":3, "반쯤감김":4, "활짝":5};
Concessions={"솜사탕":"0","재스민 차":"1","조자콜라":"2","사워 슬라임":"3","개인용 피자":"4",
    "나초":"5","연어 버거":"6","아이스크림 샌드위치":"7","팝콘":"8","감자튀김":"9",
    "초콜릿 팝콘":"10","블랙 리코리스":"11","스타 쿠키":"12","죠브레이커":"13","소금 땅콩":"14","후무스 스낵 팩":"15",
    "케일 스무디":"16","사과 슬라이스":"17","판자넬라 샐러드":"18","트러플 팝콘":"19","카푸치노 무스 케이크":"20",
    "조자콘":"21","스타드롭 셔벗":"22","락캔디":"23"
}

DayKey={"선택안함":""}|{"계절의 "+str(num)+"일":"_"+str(num) for num in range(1,29)}
FestivalDay={"선택안함":"","1일째":"_1","2일째":"_2","3일째":"_3"}
MarriageKey={"일반":"","결혼후":"marriage_"}
HeartKey={"선택안함":""}|{"하트"+str(num)+"이상":"_"+str(num) for num in range(2,11,2)}
SeasonKey={"선택안함":""}|{"계절-"+k:v+"_" for k,v in Season.items()}
Invalid_eventID={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,24,25,26,27,29,33,34,35,36,38,39,40,43,44,45,46,47,50,51,52,53,54,55,56,57,58,63,65,66,67,68,69,70,71,72,73,74,75,76,91,92,93,94,95,96,97,100,101,102,112,706,707,1237,1431,6661,6662,6663,7505,7507,7540,7550,7560,7570,7609,7610,7616,9990,9991,9992,9993,9994,9995,9996,9997,11053,11111,11151,11181,11191,11192,16000,16001,16002,16006,16007,16008,26000,35000,35001,35002,35003,35004,35004,35005,35010,35101,35110,35220,60367,69696,75001,75002,75003,75004,75005,76090,76100,76110,76120,76130,76140,76170,76180,77702,77704,77706,77708,77710,90000,90001,95278,100112,100112,100113,100113,100114,100114,100115,100115,100116,100116,100117,100117,100117,100118,100118,100162,134822,136822,138822,164822,166822,168822,181928,191393,195012,195013,195019,195099,233104,247101,247110,247111,247112,247113,247120,288847,288848,288849,318560,321777,336471,336473,336474,336475,371652,384882,384883,404798,418172,418173,418174,418175,418176,420100,420101,420102,420103,420104,420691,420693,420694,423502,463391,471942,500100,500200,500300,500400,502261,502969,503180,520702,528052,529952,529955,529956,529957,529958,529960,558291,558292,571102,584059,611173,611439,611944,639373,656565,690006,691039,696969,711130,719926,733330,739330,777111,831125,897405,900553,901756,911526,917409,958277,958279,958280,958281,958563,958563,958564,958564,958564,958564,958564,958564,958564,958564,958565,958565,958566,958566,958567,958568,958568,958569,980558,985822,992253,992553,992559,992559,1000000,1000001,1000001,1000001,1000002,1000003,1000004,1000005,1000006,1000007,1000008,1000009,1000010,1000011,1000012,1000013,1000014,1000015,1000016,1000017,1000018,1000019,1000020,1000021,1000022,1000023,1000024,1000025,1000026,1000027,1000028,1000029,1000030,1000031,1000032,1000033,1000034,1000035,1000036,1000037,1000038,1000075,1000076,1000077,1000078,1000079,1000080,1000081,1000092,1000099,1000510,1001234,1002413,1002414,1004200,1032000,1050034,1090501,1090502,1090503,1090504,1100000,1111101,1111200,1140961,1199221,1199222,1199223,1199224,1199226,1199227,1300000,1316822,1590166,1668222,1848481,1914822,1916822,1918822,1954822,1956822,1958822,2000000,2000001,2000002,2000003,2000004,2000050,2111194,2111294,2118991,2119820,2119821,2120303,2123243,2123343,2128292,2146991,2346091,2346092,2346093,2346094,2346095,2346096,2346097,2346995,2346996,2346997,2346998,2481135,2794460,3000090,3000091,3000095,3000096,3091462,3102768,3333094,3560078,3560079,3560080,3560081,3560082,3600000,3600001,3716520,3900074,3910674,3910974,3910975,3910979,3911124,3912125,3912126,3912127,3912128,3912129,3912130,3912131,3912132,3917584,3917585,3917586,3917587,3917589,3917590,3917600,3917601,3917626,3917666,3918600,3918601,3918602,3918603,4000001,4000002,4000003,4000004,4081148,4324303,4325434,4444444,4444445,4444446,4444447,4444448,4444459,4444460,4444461,4444462,4719420,5000000,5000000,5000001,5000002,5000003,5029690,5183338,5200000,5299300,5299301,5299302,5299303,6184643,6184644,6669102,6669104,6669106,6669108,6669110,6669202,6669204,6669206,6669208,6669210,6963327,7080800,7080831,7086801,7142999,7144868,7374831,7387851,7472145,7771191,8000000,8080800,8080801,8080802,8080803,8080804,8080807,8675310,8675311,8675611,9174090,9333219,9333220,9581348,9588563,9588563,9588564,9588565,9588566,9588567,9588568,9588569,9588570,9925530,9925535,9925536,9925537,9925538,9925539,9925540,9925541,9925542,9925543,9925544,10015151,10015152,10015153,10015154,10015155,10015156,10015157,10015158,10015159,10015160,10015161,10015162,10015163,10015164,10015165,10015166,10015167,10015168,10015169,10015170,10015171,10015172,10015173,10015174,10015175,10015176,10015178,13161022,15299300,15299301,15299302,15299303,15299304,15299306,15299307,15299308,15299309,15299310,15299311,15299312,15299313,16299300,16681222,17170004,17170010,37409999,40276931,40276931,40276932,40276933,52993014,59443111,59443123,59443123,59443124,59443124,59443125,59443125,59443143,59443143,59443413,66691021,66691061,66692101,101010101,101010101,101010102,101010103,103042015,111111111,111111111,111111112,111111113,111111114,111111115,111111116,131661022,191482213,200000000,222222211,282815601,282815602,282815603,282815604,282815605,282815606,282815607,282815608,282815609,282815610,282815611,282815612,282815613,282815614,282815615,282815616,282815617,282815618,282815619,282815620,282815621,282815622,282815623,282815624,282815625,282815627,282815627,282815628,282815628,282815630,282815630,282815631,303030300,303030300,303030301,303030302,333300000,404040401,404040401,404040402,404040403,444810001,444810002,444810003,444810004,444810005,444810006,444810007,444810008,505050501,505050502,505050503,808080801,808080801,808080802,808080803,1316612122,1316612222,1316612322,1316612422}

with open(os.path.join(os.getcwd(), "content","MusicList.json"), encoding="utf-8") as f:
        music_data=json.load(f)
with open(os.path.join(os.getcwd(), "content","SFXList.json"), encoding="utf-8") as f:
        sound_data=json.load(f)

def day26_transform(a,b):
    try:
        time=a*100+(b*100)//60
    except: time=int(a)*100+(int(b)*100)//60
    if 0<=time<=200:
        result=time+2400
    else:
        result=time
    return max(610,result)
def actormove_transform(user_input):
    pausedir={"오른쪽으로":"1", "아래로":"2", "왼쪽으로":"3", "위로":"4"}
    result=[]
    #/f [['위로','아래로',왼쪽으로','오른쪽으로'],5,'칸 또는 밀리초',['이동','정지']]
    for i in range(0,len(user_input),3):
        if user_input[i+2]=="정지":
            result.append(f"{pausedir[user_input[i]]} {user_input[i+1]}")
        else:
            if user_input[i]=="오른쪽으로":
                result.append(f"{user_input[i+1]} 0")
            if user_input[i]=="왼쪽으로":
                result.append(f"-{user_input[i+1]} 0")
            if user_input[i]=="위로":
                result.append(f"0 {user_input[i+1]}")
            if user_input[i]=="아래로":
                result.append(f"0 -{user_input[i+1]}")
    return " ".join(result) # 앞에 공백 안 달려있음
def generalmove_transform(dir1,num,dir2):
    result=""
    num=str(num)
    """
    c FNPCName/(이)가 /c ['위로','아래로',왼쪽으로','오른쪽으로']/ /e/칸 이동하고/c Direction/바라봄
    /n/다음 줄 즉시 실행? /c ['true','false']
    """
    if dir1=="오른쪽으로":
        result+=f"{num} 0 "
    if dir1=="왼쪽으로":
        result+=f"-{num} 0 "
    if dir1=="위로":
        result+=f"0 {num} "
    if dir1=="아래로":
        result+=f"0 -{num} "
    result+=Direction[dir2]
    return result
def add_Collin(user_input):
    if len(user_input)==1:
        return "\"#"+"".join(user_input)+"\""
    return "\"#"+"#".join(user_input)+"\""
def create_questionnull(NPC,user_input):
    choose=[]
    response=[]
    for i in range(0,len(user_input),2):
        choose.append(user_input[i])
        response.append(user_input[i+1])
    result="question null \"#"+"#".join(choose)+"\""+"/pause 500"+f"/splitSpeak {NPC} \""+"~".join(response)+"\""
    return result
def addeventdial(message):
    return f"\"{message}\""
def locationandxy():
    lc=select_location(None,False,False)
    return f"{lc[0]} {lc[1]} {lc[2]}"
def replace_blank(s):
    return s.replace(" ","_")

# 현재 날짜와 시간을 'YYYYMMDD_HHMMSS' 형태로 생성-npc의 영어이름 대신 활용
def make_unique_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
# manifest.json 내용 생성
def create_manifest(name): #uid 생성 점검
    author = "MyStardewNPC"
    uid = make_unique_id()
    return {
        "Name": f"[CP] {name} by {author}",
        "Author": author,
        "Version": "1.0.0",
        "Description": f"{name} 캐릭터를 추가하는 스타듀밸리 Content Patcher 모드입니다.",
        "UniqueID": f"{uid}.customnpc",
        "ContentPackFor":
        {
            "UniqueID": "Pathoschild.ContentPatcher",
            }
    }
# content.json 기본 구조 생성
def create_content(name, values, entry_id=None):
    if not entry_id:
        global root
        win=tk.Toplevel(root)
        tk.Label(win, text="영어 이름 입력(매우 중요)").pack(side="top")
        nameE=tk.Entry(win,width=15);nameE.pack(side="top")
        def complete_handler():
            Enname=nameE.get()
            if Enname:
                if re.fullmatch(r'[A-Za-z0-9]+', Enname):
                    nonlocal entry_id
                    entry_id = Enname
                    win.destroy()
                else:
                    messagebox.showerror("오류","영어와 숫자 이외의 문자는 불가능합니다")
                    return
            else:
                messagebox.showerror("오류","공백은 불가합니다")
                return
        complete_btn=tk.Button(win,text="완료",command=complete_handler)
        complete_btn.pack(side="top")
        #만약에 win창이 존재한다면 win이 destory될 때까지 기다리기
        win.grab_set()
        root.wait_window(win)
    values["DisplayName"] = name
    return {
        "Format": "2.0.0",
        "Changes": [
            {
                "Action": "EditData",
                "Target": "Data/Characters",
                "Entries":
                {
                    entry_id: values
                }
            }
        ]
    }
# 프로젝트 폴더 및 기본 파일 생성
def create_project_folder(name, values,entry_id=None):
    author = "MyStardewNPC"
    folder = f"[CP] {name} by {author}"
    exp_dir = os.path.join("export", folder)
    os.makedirs(exp_dir, exist_ok=True)
    for sub in ["dialogue", "portraits", "schedules", "sprites"]:
        os.makedirs(os.path.join(exp_dir, sub), exist_ok=True)
    with open(os.path.join(exp_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(create_manifest(name), f, indent=4, ensure_ascii=False)
    with open(os.path.join(exp_dir, "content.json"), "w", encoding="utf-8") as f:
        json.dump(create_content(name, values,entry_id), f, indent=4, ensure_ascii=False)
    return exp_dir 
#entry_id는 영어이름, 유저에게 입력 받아야

# content.json 불러오기 및 수정 모듈
def load_content_json(dirpath):
    try:
        with open(os.path.join(dirpath, "content.json"), encoding="utf-8") as f:
            return json.load(f)
    except:
        with open(os.path.join(dirpath, "content.json"), encoding="utf-8-sig") as f:
            return json.load(f)
def load_unique_id(data=None):
    if not data:
        data = load_content_json(project_dir)
    try:
        entries = data["Changes"]
        for change in entries:
            if change["Target"]=="Data/Characters":
                id = list(change["Entries"].keys())[0]
                if not id in NPCName:
                    NPCName.append(id)
                    FNPCName.append(id)
                return id
    except Exception:
        return None
#bool함수 로맨스가 가능한가?
def isromance(data=None):
        """content.json 에서 CanBeRomanced 값을 읽어옴"""
        try:
            if not data:
                data = load_content_json(project_dir)
            entries = data["Changes"]
            for change in entries:
                if change["Target"]=="Data/Characters":
                    entries = change["Entries"]
                    vals = list(entries.values())[0]
                    return vals["CanBeRomanced"]
        except Exception:
            return False
def load_animation_data(lines=None): #인덱스/액션이름/액션순번 정보 불러옴
    new_anims={}
    if lines==None:
        characterID=load_unique_id()
        txt_path = os.path.join(os.getcwd(), "content", "user_data", "animation_data", f"{characterID}.txt")
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    lines=sorted(lines)
    for line in lines:
        linelist=line.split("/")
        if linelist[1].split():
            if linelist[1] in new_anims:
                while len(new_anims[linelist[1]])<=int(linelist[2]):
                    new_anims[linelist[1]].append(0)
                new_anims[linelist[1]][int(linelist[2])]=int(linelist[0])
            else:
                if int(linelist[2])==0:
                    new_anims[linelist[1]]=[int(linelist[0])]
                else:
                    while len(new_anims[linelist[1]])<=int(linelist[2]):
                        new_anims[linelist[1]].append(0)
                    new_anims[linelist[1]][int(linelist[2])]=int(linelist[0])
    return new_anims
def load_event_info(data=None): #(장소, 이름, eid) 튜플의 리스트
    if not data:
        data = load_content_json(project_dir)
    character_name=load_unique_id(data)
    path = os.path.join("content", "user_data", "event_data", f"{character_name}.txt")
    result = []
    if not os.path.exists(path):
        return result
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "/" not in line:
                continue
            parts = line.strip().split("/")
            if len(parts) == 3:
                place, name, eid = parts
                result.append((place, name, eid))
    return result
def get_event_name_by_id(eid,info=None):#이벤트 id로 이름알아냄
    if not info:
        data = load_content_json(project_dir)
        info = load_event_info(data)
    for place, name, event_id in info:
        if event_id == eid:
            return name
    return ""
#(장소, 이름, eid) 튜플의 리스트
def load_events_from_json(data=None): #content.json에서 모든 이벤트 가져옴
    if not data:
        data = load_content_json(project_dir)
    event_entries = {}
    changes = data["Changes"]
    for change in changes:
        if change.get("Action") == "EditData":
            target=change.get("Target")
            if target.startswith("Data/Events/"):
                location = target.split("/")[-1]
                event_entries[location]=[]
                entry_dict= change.get("Entries")
                #change.get("Entries")는 key/스크립트val로 이루어진 dict
                for k, v in entry_dict.items():
                    key=k.split("/")[0] #event ID
                    val=v.split("\"")[1] #첫번째로 존재하는 대사
                    event_entries[location].append((key,val,k,v))
    return event_entries #location key와 이벤트 튜플로 이루어진 list val 반환 
def load_response_info(data=None):
    if not data:
        data = load_content_json(project_dir)
    character_name=load_unique_id(data)
    path = os.path.join("content", "user_data", "response_data", f"{character_name}.txt")
    result = []
    if not os.path.exists(path):
        return result
    with open(path, encoding="utf-8") as f:
        for line in f:
            if ":" not in line:
                continue
            parts = line.strip().split(":")
            if len(parts) == 3:
                name, qid, info= parts
                result.append((name, qid, info))
    return result
def is_existing_data(values, data=None): #기존의 데이터가 존재하느냐? 있다면 수정해야 할 changes의 인덱스 반환, 없다면 0
        if not data:
            data = load_content_json(project_dir)
        changesF=data["Changes"]
        for index, i in enumerate(changesF):
            if i["Action"]==values["Action"]:
                if i["Target"]==values["Target"]:
                    if i["Action"]=="EditData":
                        return index
                    try:
                        if i["FromFile"]==values["FromFile"]:
                            return index
                    except:
                        return index
        return 0
def append_to_content(values, data=None, index=0):
    if not data:
        data = load_content_json(project_dir) #content.json의 모든 데이터
    target_to_modify=index
    if target_to_modify:
        data["Changes"][target_to_modify]=values
        #data.setdefault(key, []).append(item)
    else:
        data["Changes"].append(values)
    with open(os.path.join(project_dir, "content.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

#UI
root = tk.Tk()
root.title("스듀 NPC 생성기")
#______________________시작 프레임: 이름 입력 & 생성/불러오기______________________
start_frame = tk.Frame(root)
tk.Label(start_frame, text="캐릭터 이름").grid(row=0, column=0)
entry_name = tk.Entry(start_frame)
entry_name.grid(row=0, column=1)

# 전역으로 선택된 프로젝트 경로 저장
project_dir = None
# 생성 버튼
def on_create():
    name = entry_name.get().strip()
    if not name:
        return messagebox.showerror("오류", "캐릭터 이름을 입력하세요.")
    # 기본 정보 폼 띄우기
    start_frame.pack_forget()
    form_frame.pack(padx=10, pady=10)
# 불러오기 버튼
def on_load():
    name = entry_name.get().strip()
    if not name:
        return messagebox.showerror("오류", "불러올 캐릭터 이름을 입력하세요.")
    exp = os.path.join(os.getcwd(), "export")
    folder = f"[CP] {name} by MyStardewNPC"
    proj = os.path.join(exp, folder)
    if not os.path.isdir(proj):
        on_create()
        return
    global project_dir
    project_dir = proj
    start_frame.pack_forget()
    open_advanced_form()
tk.Button(start_frame, text="생성 또는 불러오기", command=on_load).grid(row=1, column=1, padx=5)
start_frame.pack(padx=10, pady=10)

#호출될 시 맵과 좌표, 이동방향을 선택할 수 있는 화면을 띄우고 종료 시 (mapname,x,y,direction) 튜플 반환
#isdirection=True가 아니면 아무키나 눌러서 좌표만 반환, 이에 따라 라벨도 수정
def select_location(mapname=None, numdirection=False, isdirection=True):
    maps_dir = os.path.join(os.getcwd(), "content", "mapdata")
    if not os.path.isdir(maps_dir):
        messagebox.showerror("오류", "mapdata 폴더가 없습니다.")
        return None
    maps = [f for f in os.listdir(maps_dir)
            if os.path.isfile(os.path.join(maps_dir, f)) and f.lower().endswith(".png")]+["Desert","Club","AndyHouse","eachNightMarket"]
    if not maps:
        messagebox.showerror("오류", "등록된 PNG 맵 파일이 없습니다.")
        return None

    # ── 1) 맵 선택 콤보박스 다이얼로그 ──
    if mapname==None:
        map_names = [os.path.splitext(f)[0] for f in maps]  # 확장자 제거
        sel_win = tk.Toplevel()
        sel_win.title("맵 선택")
        tk.Label(sel_win, text="맵 파일을 선택하거나 직접 입력:").pack(anchor="w", padx=10, pady=(10, 0))

        combo = ttk.Combobox(sel_win, values=map_names)
        combo.set(map_names[0])
        combo.pack(fill="x", padx=10, pady=5)

        chosen = tk.StringVar()
        def on_confirm():
           chosen.set(combo.get().strip())
           sel_win.destroy()
            
        def on_cancel():
            chosen.set("")
            sel_win.destroy()

        btn_frame = tk.Frame(sel_win)
        tk.Button(btn_frame, text="확인", command=on_confirm).pack(side="left", padx=5)
        tk.Button(btn_frame, text="취소", command=on_cancel).pack(side="left", padx=5)
        btn_frame.pack(pady=(0, 10))

        sel_win.grab_set()
        sel_win.wait_window()

        val = chosen.get()
        if not val:
            return None
    else:
        val=mapname

    img_path = os.path.join(maps_dir, val + ".png")
    # — 파일이 없으면 사용자 직접 입력
    if not os.path.isfile(img_path):
        dlg = tk.Toplevel(root)
        dlg.title("직접 좌표 입력")
        dlg.geometry("300x180")
        dlg.resizable(False, False)

        # 맵 이름
        # — 맵 이름 (굵은 글씨) —
        tk.Label(dlg, text=f"{val} 맵에서", font=("맑은고딕", 11, "bold")) \
        .grid(row=0, column=0, columnspan=6, pady=(10, 5), sticky="w")

        # 좌표·방향 입력 영역을 별도 Frame에 그룹화
        coord_frame = tk.Frame(dlg)
        coord_frame.grid(row=1, column=0, columnspan=6, padx=10, pady=(0,10), sticky="w")

        # X 좌표
        tk.Label(coord_frame, text="X:").pack(side="left", padx=(0,4))
        entry_x = tk.Entry(coord_frame, width=5)
        entry_x.pack(side="left")
        entry_x.insert(0, "0")

        # Y 좌표
        tk.Label(coord_frame, text="Y:").pack(side="left", padx=(10,4))
        entry_y = tk.Entry(coord_frame, width=5)
        entry_y.pack(side="left")
        entry_y.insert(0, "0")

        if isdirection:
            # 방향 콤보박스
            tk.Label(coord_frame, text="방향:").pack(side="left", padx=(10,4))
            dir_var = tk.StringVar(dlg)
            directions = ["up", "down", "left", "right"]
            combo_dir = ttk.Combobox(coord_frame, textvariable=dir_var, values=directions, state="readonly", width=6)
            combo_dir.pack(side="left")
            combo_dir.current(0)

        result = {"map": None, "x": 0, "y": 0, "Direction": None}

        def on_ok():
            try:
                result["map"] = val
                result["x"] = int(entry_x.get())
                result["y"] = int(entry_y.get())
                if isdirection:
                    result["Direction"] = dir_var.get()
                dlg.destroy()
            except ValueError:
                messagebox.showerror("오류", "좌표는 정수여야 합니다.")

        def on_cancel():
            dlg.destroy()

        btn_frame = tk.Frame(dlg)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="확인", width=10, command=on_ok).pack(side="left", padx=5)
        tk.Button(btn_frame, text="취소", width=10, command=on_cancel).pack(side="left")

        dlg.grab_set()
        dlg.wait_window()

        # 사용자가 확인을 누르고 dlg가 destroy 된 후
        if result["map"] is None:
            return None
        if numdirection:
            if result["Direction"]=="up":
                result["Direction"]="0"
            elif result["Direction"]=="right":
                result["Direction"]="1"
            elif result["Direction"]=="down":
                result["Direction"]="2"
            elif result["Direction"]=="left":
                result["Direction"]="3"
        return result["map"], result["x"], result["y"], result["Direction"]

    # ── 2) 좌표/방향 선택 ──
    top = tk.Toplevel()
    top.title(f"위치 선택 — {val}")

    orig = Image.open(img_path)
    w, h = orig.size

    # (1) 절반 크기로 축소할 때 LANCZOS 사용
    disp = orig.resize((w // 3, h // 3), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(disp)

    # (2) 안내문구를 최상단에 배치
    if isdirection:
        instr = tk.Label(top,
                        text="클릭으로 좌표 선택, 휠로 줌, ←↑→↓ 로 방향 지정",
                        font="맑은고딕 10 bold"
                        )
        instr.pack(pady=5)
    else:
        instr = tk.Label(top,
                        text="클릭으로 좌표 선택, 휠로 줌, 아무 키나 눌러 종료",
                        font="맑은고딕 10 bold"
                        )
        instr.pack(pady=5)

    canvas = tk.Canvas(top, width=disp.width, height=disp.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor ="nw", image=tk_img)

    if isdirection:
        coord_lbl = tk.Label(top, text="현재: X=0, Y=0, 방향=none")
    else:
        coord_lbl = tk.Label(top, text="현재: X=0, Y=0")
    coord_lbl.pack(pady=(5, 10))
    result = {"Map": val, "X": 0, "Y": 0, "Direction": "down"}
    marker = None #??
    scale = 1.0

    def on_click(evt):
        nonlocal marker
        ox, oy = evt.x * 2 / scale, evt.y * 2 / scale
        tx, ty = int(ox * 129 / w), int(oy * 129 / h)
        result["X"], result["Y"] = tx, ty
        if marker:
            canvas.delete(marker)
        marker = canvas.create_oval(evt.x - 5, evt.y - 5, evt.x + 5, evt.y + 5,
                                    outline="red", width=2)
        if isdirection:
            coord_lbl.config(text=f"현재: X={tx}, Y={ty}, 방향={result['Direction']}")
        else: coord_lbl.config(text=f"현재: X={tx}, Y={ty}")
    def on_key(evt):
        k = evt.keysym.lower()
        if not isdirection:
            top.destroy()
        elif k in ("left", "right", "up", "down"):
            result["Direction"] = k
            coord_lbl.config(text=f"현재: X={result['X']}, Y={result['Y']}, 방향={k}")
            top.destroy()
    def on_zoom(evt):
        nonlocal scale, tk_img
        delta = evt.delta if hasattr(evt, "delta") else (1 if evt.num == 4 else -1)
        factor = 1.1 if delta > 0 else 0.9
        scale *= factor

        nw, nh = int(disp.width * scale), int(disp.height * scale)
        resized = disp.resize((nw, nh), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(resized)

        canvas.config(width=nw, height=nh)
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=tk_img)

        if result["X"] or result["Y"]:
            mx = result["X"] * (nw / 129)
            my = result["Y"] * (nh / 129)
            canvas.create_oval(mx - 5, my - 5, mx + 5, my + 5, outline="red", width=2)

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<MouseWheel>", on_zoom)
    canvas.bind("<Button-4>", on_zoom)
    canvas.bind("<Button-5>", on_zoom)
    top.bind("<Key>", on_key)
    canvas.focus_set()
    top.grab_set()
    root.wait_window(top)
    if numdirection:
        if result["Direction"]=="up":
            result["Direction"]="0"
        elif result["Direction"]=="right":
            result["Direction"]="1"
        elif result["Direction"]=="down":
            result["Direction"]="2"
        elif result["Direction"]=="left":
            result["Direction"]="3"
    return (result["Map"], result["X"], result["Y"], result["Direction"])
#방향키 안 누르고 닫아도 기본폼에 위치 표시되는 이유?
def random_number_generate(leng, values=[]):
    mi = 10 ** (leng - 1)
    ma = mi * 10 - 5

    # 모든 값이 이미 존재할 경우 대비
    if len(values) >= (ma - mi + 1):
        raise ValueError("가능한 숫자 범위를 초과했습니다.")

    while True:
        result = random.randrange(mi, ma)
        if result not in values:
            return result
def random_alpha_generate(leng=10):
    result=""
    for i in range(leng):
        if random.random()<0.5:
            result+=chr(random.randint(65,90))
        else:
            result+=chr(random.randint(97,122))
    return result
def generate_pastel_color():
    base = 200  # 최소 밝기 (127~255 사이 추천)
    r = random.randint(base, 255)
    g = random.randint(base, 255)
    b = random.randint(base, 255)
    return f'#{r:02x}{g:02x}{b:02x}'
def append_to_schedule(new_item):
    filepath=os.path.join(project_dir, "schedules", load_unique_id()+".json")
    data = {}

    # 파일이 존재하면 읽고 append
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # 내용이 비었거나 잘못된 경우
                data = []
    for k,v in new_item.items():
        data[k]=v
    # 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def append_to_dialogue(new_item, marriged=False,generalmarriged=False):
    if not marriged:
        filepath=os.path.join(project_dir, "dialogue", load_unique_id()+".json")
    elif generalmarriged:
        filepath=os.path.join(project_dir, "dialogue", "MarriageDialogue.json")
    else:
        filepath=os.path.join(project_dir, "dialogue", "MarriageDialogue"+load_unique_id()+".json")
    data = {}

    # 파일이 존재하면 읽고 append
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # 내용이 비었거나 잘못된 경우
                data = {}
    for k,v in new_item.items():
        data[k]=v
    # 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def remove_bracket(token):
    read=True;result=""
    for al in token:
        if al=="<":read=False
        elif al==">":read=True
        elif read:
            result+=al
    return result
def open_text_editor(message: str=None,isevent=False) -> str:
    dlg = tk.Toplevel()
    dlg.title("대사 편집기")
    dlg.geometry("700x500")
    dlg.resizable(False, False)
    dlg.grab_set()
    # 블럭 정의: (카테고리, [ (표시문구, 토큰), ... ], 배경색)
    BLOCKS = [
        ("표정", [("기본", "$0"), ("^-^", "$1"), ("ㅠㅠ", "$2"), ("특수", "$3"), ("♥", "$4"), ("ꐦ", "$5"),("표정 <6>","$<0>")], "#fff9c4"),
        ("제어/흐름", [("다음을 누르면 계속", "#$b#"), ("다시 말 걸어보면", "#$e#")], "#c8e6c9"),
        ("조건/랜덤", [("<5>x10% 확률로 <어이!>(이)라고 말하고, 아니면...", "$c 0.<0>#<1>#"),
                   ("<stateID:bus>이면 <아멘>(이)라고 말하고, 아니면...", "$d <0>#<1>|"),
                   ("처음이라면 <저리가>(이)라고 말하고, 아니면...","#$1 <-1>#<0>$k#$e#"),
                   ("<query:>상태라면 <오랜만이네!>(이)라고 말하고, 아니면...", "$query <0>#<1>|"),
                   ("<responseID:None>라고 답한 적이 있다면 <오케이>라고 말하고, 아니면...", "$p <0>#<1>|"),
                   ("남자에게는 <텍스트> 여자에게는 <텍스트>라고 말한다","<0>^<1>")], "#bbdefb"),
        ["질문/선택지", [
                    ], "#e1bee7"],
        ("명사삽입", [("농부이름", "@"), ("랜덤장소", "%place"), ("랜덤형용사", "%adj"),("랜덤명사","%noun"),("랜덤이름","%name"), ("농장명", "%farm"),
                  ("배우자", "%spouse"),("펫이름","%pet"),("당신이 가장 좋아하는 것","%favorite"),("당신 이름의 줄임말","%firstnameletter"),
                  ("자식1이름","%kid1"),("자식2이름","%kid2"),("현재시간","%time"),("샘세바스찬의 밴드","%band"),("엘리엇의 책","%book")], "#ffe0b2"),
        ("시스템",[("일반 텍스트 상자로 변경","%"),
                ("스페셜이벤트변수(포크) 참으로 변경 (이 뒤에 문자열X)","%fork"),
                ("<-500>원의 변화 (이 뒤에 문자열X)","#$action AddMoney <0>"),
                ("하루동안 <buffID:None> 버프 부여 (이 뒤에 문자열X)","#$action AddBuff <0>"),
                ("<NPC:Penny>프로필에 공개 취향 <itemID:168>추가하기 (이 뒤에 문자열X)","%revealtaste:<0>:<1>"),
                ("<itemIDs:168 334 27>중 하나를 준다","[<0>]")], "#8f8f8f")
    ]
    condi=[("stateID",{"버스수리됨":"bus","조자영업중":"joja","센터접근가능":"cc","켄트계곡귀환":"kent"}),
               ["responseID",{}],
               ["itemID",{}],
               ["NPC",NPCName]]
    for k,v in sd_items.items():
        if v.id>0:
            condi[2][1][k]=v.id

    #나중에 쿼리 매니저도 할 수 있다면...

    # ─── 스크롤 가능한 파레트 컨테이너 ─────────
    palette_container = tk.Frame(dlg)
    palette_container.pack(side="left", fill="y", padx=5, pady=5)

    palette_canvas = tk.Canvas(palette_container, width=200)
    scrollbar     = tk.Scrollbar(palette_container, orient="vertical", command=palette_canvas.yview)
    palette_frame = tk.Frame(palette_canvas)

    palette_canvas.configure(yscrollcommand=scrollbar.set)
    palette_canvas.pack(side="left", fill="y", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 프레임을 캔버스 안에 넣고 이벤트 바인딩
    palette_canvas.create_window((0,0), window=palette_frame, anchor="nw")
    palette_frame.bind(
        "<Configure>",
        lambda e: palette_canvas.configure(scrollregion=palette_canvas.bbox("all"))
    )
    # ─────────────────────────────────────────────

    text = tk.Text(dlg, width=60, height=30, wrap="word")
    text.pack(fill="both", expand=True, padx=5, pady=5)

    #간단한 질문 관리자
    def simple_question():
        dlg2 = tk.Toplevel(dlg)
        dlg2.title("간단한 질문 관리자")
        dlg2.geometry("800x300")
        top_container=tk.Frame(dlg2);top_container.pack(side="top") #\n(이 뒤에 문자열X)
        tk.Label(top_container,text="제목").pack(side="left")
        titlebox=tk.Entry(top_container, width=15);titlebox.pack(side="left")
        tk.Label(top_container,text="   질문").pack(side="left")
        qbox=tk.Entry(top_container, width=40, state="readonly");qbox.pack(side="left")
        def qadd_handler(qbox=qbox):
            qbox.config(state="normal")
            qbox.delete(0,tk.END)
            textd=qbox.get()
            if textd=="end" or textd=="":
                textd=open_text_editor(isevent=isevent)
            else: textd=open_text_editor(message=textd, isevent=isevent)
            qbox.insert(0,textd)
            qbox.config(state="readonly")
        qadd=tk.Button(top_container,text="대사",command=qadd_handler);qadd.pack(side="left")

        create_dynamic_input(dlg2,values=['   선택지',40,'NPC반응',lambda: open_text_editor(isevent=isevent)],side="top",btn_text="대사",res_width=40)
        def add_block(qbox=qbox,dlg2=dlg2):
            QNA=""
            for widget in dlg2.winfo_children():
                if isinstance(widget,tk.Frame):
                    for wid in widget.winfo_children():
                        if isinstance(wid,tk.Entry):
                            if not wid.get():
                                messagebox.showerror("오류", "공백은 불가합니다")
                                return
                            if wid==qbox:
                                QNA=wid.get()
                            else: qtitle=wid.get()
                        elif isinstance(wid,tk.Frame):
                            for wd in wid.winfo_children():
                                if isinstance(wd,tk.Entry):
                                    if not wd.get():
                                        messagebox.showerror("오류", "공백은 불가합니다")
                                        return
                                    QNA+="_"+wd.get()
            BLOCKS[3][1].append((qtitle+"(이 뒤에 문자열X)","$y '"+QNA+"'"))
            update_block()
            dlg2.destroy()
        tk.Button(top_container,text="블록추가(완료)",command=add_block).pack(side="left",padx=5)
    #표준 질문 관리자(isevent 여부 따라 편집해야함)
    def advanced_question():
        QNADial=[]
        qtitle=""
        answerkey=[]
        dlg2 = tk.Toplevel(dlg)
        dlg2.title("표준 질문 관리자")
        dlg2.geometry("800x400")
        top_container=tk.Frame(dlg2);top_container.pack(side="top")
        tk.Label(top_container,text="제목(영문)").pack(side="left")
        titlebox=tk.Entry(top_container, width=15);titlebox.pack(side="left")
        titlebox.insert(0,"title");
        tk.Label(top_container,text="   질문").pack(side="left")
        qbox=tk.Entry(top_container, width=40, state="readonly");qbox.pack(side="left")
        def qadd_handler(qbox=qbox):
            qbox.config(state="normal")
            textd=qbox.get()
            qbox.delete(0,tk.END)
            if textd=="end" or textd=="":
                textd=open_text_editor(isevent=isevent)
            else: textd=open_text_editor(message=textd, isevent=isevent)
            qbox.insert(0,textd)
            qbox.config(state="readonly")
        qadd=tk.Button(top_container,text="대사",command=qadd_handler);qadd.pack(side="left")
        if not isevent:
            tk.Label(dlg2,text="yes, no, gobeach 등의 분기를 입력해주세요.\n선택지의 개수와 분기의 개수는 같지 않을 수도 있습니다.\n[1. 선택지/분기 수 지정] -> [2. 선택지 및 응답 입력] -> [3. fallback 지정]").pack(side="top")
        else: tk.Label(dlg2,text="yes, no, gobeach 등의 분기를 입력해주세요.\n선택지의 개수와 분기의 개수는 같지 않을 수도 있습니다.\n[1. 선택지/분기 수 지정] -> [2. 선택지 및 응답 입력]").pack(side="top")
        blank="                                                                        "
        clen_c=tk.Frame(dlg2);clen_c.pack(side="top")
        tk.Label(clen_c,text=blank+"플레이어 선택지 개수:").pack(side="left");tk.Entry(clen_c,width=5).pack(side="left")
        create_dynamic_input(dlg2,values=[blank+"title_",10],side="top")
        
        def last_step(qtitle, rids,QNADial):
            if not isevent:
                tk.Label(dlg2,text="마지막으로, 질문에 이미 답변한 적이 있을 때 NPC가 보일 반응을 설계해 봅시다").pack(side="top")
                title=qtitle+"_old"
                tk.Label(dlg2,text=title).pack(side="top")
                container=tk.Frame(dlg2);container.pack(side="top")
                roldbox=tk.Entry(container, width=40, state="readonly");roldbox.pack(side="left")
                def qadd_handler():
                    roldbox.config(state="normal")
                    textd=roldbox.get()
                    roldbox.delete(0,tk.END)
                    if textd=="end" or textd=="":
                        textd=open_text_editor(message="[<responseID:"+rids[0]+">라고 답한 적이 있다면 <오케이>라고 말하고, 아니면...]",isevent=isevent)
                    else: textd=open_text_editor(message=textd, isevent=isevent)
                    roldbox.insert(0,textd)
                    roldbox.config(state="readonly")
                qadd=tk.Button(container,text="대사",command=qadd_handler);qadd.pack(side="left")

            def on_complete_q():
                if not isevent:
                    old_dial=roldbox.get()
                    if not old_dial:
                        messagebox.showerror("오류","공백은 불가능합니다")
                        return
                    append_to_dialogue({title:old_dial})
                result_str="#$q "+"/".join(rids)+" "+title+"#"+"".join(QNADial)
                BLOCKS[3][1].append((qtitle+"(이 뒤에 문자열X)",result_str))
                update_block()
                dlg2.destroy()
            
            tk.Button(dlg2,text="완료",command=on_complete_q).pack(side="bottom",padx=5,pady=5)
            if isevent:
                title="null"
                rids=[rids[0]]
                on_complete_q()
        def on_select_next(qbox=qbox,clen_c=clen_c, dlg2=dlg2):
            nonlocal QNADial
            nonlocal qtitle
            nonlocal answerkey
            clen=0
            QNADial.clear();qtitle="";answerkey.clear()
            for widget in dlg2.winfo_children():
                if isinstance(widget,tk.Frame):
                    for wid in widget.winfo_children():
                        if isinstance(wid,tk.Entry):
                            val=wid.get()
                            if not val:
                                messagebox.showerror("오류", "공백은 불가합니다")
                                return
                            elif widget==clen_c:
                                try: clen=int(val)
                                except:
                                    messagebox.showerror("오류", "정수만 입력할 수 있습니다")
                                    return
                            elif not (qbox or re.fullmatch(r'[A-Za-z0-9]+', val)):
                                messagebox.showerror("오류", "영어나 숫자만 입력할 수 있습니다")
                                return
                            else:
                                if wid==qbox:
                                    QNADial.append(val)
                                else: qtitle=val
                        elif isinstance(wid,tk.Frame):
                            for wd in wid.winfo_children():
                                if isinstance(wd,tk.Entry):
                                    val=wd.get()
                                    if not val:
                                        messagebox.showerror("오류", "공백은 불가합니다")
                                        return
                                    if not re.fullmatch(r'[A-Za-z0-9]+', val):
                                        messagebox.showerror("오류", "영어나 숫자만 입력할 수 있습니다")
                                        return
                                    else:
                                        answerkey.append(qtitle+"_"+val)
            for widget in dlg2.winfo_children():                            
                widget.destroy()

            tk.Label(dlg2,text=QNADial[0]).pack(side="top")
            userinput=tk.Frame(dlg2);userinput.pack()
            ccontainer=tk.Frame(userinput);ccontainer.pack(side="left") #chosen container
            rcontainer=tk.Frame(userinput);rcontainer.pack(side="right") #response container
            crow=[];
            for i in range(clen):
                row=tk.Frame(ccontainer);row.pack(side="top",pady=5,padx=5)
                row1=tk.Frame(row);row1.pack(side="top")
                tk.Label(row1,text="   선택지").pack(side="left")
                tk.Entry(row1,width=40).pack(side="left")
                row2=tk.Frame(row);row2.pack(side="top")
                tk.Label(row2,text="   연결").pack(side="left")
                ttk.Combobox(row2,width=15, values=answerkey,state="readonly").pack(side="left")
                tk.Label(row2,text="   호감도").pack(side="left")
                tk.Entry(row2,width=5).pack(side="left")
                tk.Label(row2,text="포인트").pack(side="left")
                row3=tk.Frame(row);row3.pack(side="top")
                var=tk.BooleanVar(value=False)
                res_match_cb=ttk.Combobox(row3,values=list(condi[1][1].keys()),state="disabled");
                def chkhandler(var=var,res_match_cb=res_match_cb):
                    if var.get():
                        res_match_cb.config(state="readonly")
                        res_match_cb.current(0)
                    else:
                        res_match_cb.set("")
                        res_match_cb.config(state="disabled")
                chk=tk.Checkbutton(row3,text="이전의 응답",variable=var,command=chkhandler);chk.pack(side="left")
                res_match_cb.pack(side="left")
                tk.Label(row3,text="과(와) 같은 id 사용").pack(side="left")
                chk.pack(side="left",padx=5,pady=5)
                crow.append([row1,row2,row3])
            tk.Label(rcontainer,text="NPC응답").pack(side="top",pady=10)
            for key in answerkey:
                row=tk.Frame(rcontainer);row.pack(side="top")
                tk.Label(row,text=key+":").pack(side="left",padx=5,pady=5)
                ebox=tk.Entry(row, width=40, state="readonly");ebox.pack(side="left",padx=5,pady=5)
                def eadd_handler(ebox=ebox):
                    ebox.config(state="normal")
                    textd=ebox.get()
                    ebox.delete(0,tk.END)
                    if textd=="end" or textd=="":
                        textd=open_text_editor(isevent=isevent)
                    else: textd=open_text_editor(message=textd, isevent=isevent)
                    ebox.insert(0,textd)
                    ebox.config(state="readonly")
                qadd=tk.Button(row,text="대사",command=eadd_handler);qadd.pack(side="left",padx=5,pady=5)
            tk.Label(rcontainer,text="이전의 응답과 동일한 id를 사용하여\n같은 질문을 여러번 하는 일을 막을 수 있습니다").pack(side="top",pady=10)
            def step3_go_handler():
                nonlocal clen;id_min=random_number_generate(5,list(condi[1][1].values()))
                nonlocal QNADial;nonlocal qtitle;nonlocal answerkey; nonlocal rcontainer
                dials=[];rids=[];connections=[];hearts=[]
                new_items={}
                for token in crow:
                    for widget in token[0].winfo_children():
                        if isinstance(widget,tk.Entry):
                            val=widget.get()
                            if not val:
                                messagebox.showerror("오류","공백은 불가능합니다")
                                return
                            dial=val
                    for widget in token[1].winfo_children():
                        if isinstance(widget,ttk.Combobox):
                            val=widget.get()
                            if not val:
                                messagebox.showerror("오류","공백은 불가능합니다")
                                return
                            connection=val
                        if isinstance(widget,tk.Entry):
                            val=widget.get()
                            if not val:
                                messagebox.showerror("오류","공백은 불가능합니다")
                                return
                            heart=val
                    for widget in token[2].winfo_children():
                        if isinstance(widget,tk.Entry):
                            val=widget.get()
                            if val:
                                rid=condi[1][1][val]
                            else:
                                while str(id_min) in list(condi[1][1].values()):
                                    id_min+=1
                                rid=str(id_min); id_min+=1
                    dials.append(dial);rids.append(rid) #response ids
                    connections.append(connection); hearts.append(heart)
                for token in rcontainer.winfo_children():
                    if isinstance(token,tk.Frame):
                        for tok in token.winfo_children():
                            if isinstance(tok, tk.Entry):
                                dial=tok.get()
                                if not dial:
                                    messagebox.showerror("오류","공백은 불가합니다")
                                    return
                            if isinstance(tok, tk.Label):
                                rtitle=tok.cget("text")
                        new_items[rtitle[:-1]]=dial
                character_name=load_unique_id() #responsedata 업데이트
                filepath = os.path.join("content", "user_data", "response_data", f"{character_name}.txt")

                line_num = None
                # 파일이 존재하면 읽고 append 위치 계산
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    # line_num이 없거나 유효하지 않으면 파일 끝에 추가
                    if not isinstance(line_num, int) or line_num < 1:
                        line_num = len(lines) + 1
                    elif line_num > len(lines) + 1:
                        line_num = len(lines) + 1
                else:
                    lines = []
                    line_num = 1  # 새 파일이면 처음부터 삽입
                # 줄 삽입 및 저장
                for i in range(clen):
                    QNADial.append(f"#$r {rids[i]} {hearts[i]} {connections[i]}#{dials[i]}")
                    lines.insert(line_num - 1 + i, f"{dials[i]}:{rids[i]}:{connections[i]}\n")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                append_to_dialogue(new_items)
                for widget in dlg2.winfo_children():                     
                    widget.destroy()
                last_step(qtitle, rids,QNADial)
            tk.Button(dlg2,text="다음(누르면 되돌릴 수 없습니다!)",command=step3_go_handler).pack(side="bottom",padx=5,pady=5)
        tk.Button(dlg2,text="다음",command=on_select_next).pack(side="bottom",padx=5,pady=5)
    def insert_block(label, tag):
        text.insert(tk.INSERT, f"[{label}]", tag)

    block_container=tk.Frame(palette_frame);block_container.pack(fill="x", pady=(10,2), padx=2)
    condi_container=tk.Frame(palette_frame);condi_container.pack(fill="x", pady=(10,2), padx=2)
    def update_condi():
        for widget in condi_container.winfo_children():
            widget.destroy()
        response_data=load_response_info()
        for tok in response_data:
            condi[1][1][tok[2]+tok[0]]=tok[1]
        color="#cfd8dc"
        
        lbl = tk.Label(condi_container, text="<변수삽입>", bg=color, font=("맑은고딕", 10, "bold"))
        lbl.pack(fill="x", pady=(10,2), padx=2)
        
        for ctg, item in condi:
            # 카테고리 라벨
            lbl = tk.Label(condi_container, text=ctg+":", bg=color, font=("맑은고딕", 10, "bold"))
            lbl.pack(fill="x", pady=(10,2), padx=2)
            if isinstance(item,dict):
                con_cb=ttk.Combobox(condi_container, values=list(item.keys()),font=("맑은고딕", 10, "bold"),state="readonly")
            else:
                con_cb=ttk.Combobox(condi_container, values=item,font=("맑은고딕", 10, "bold"),state="readonly")
            con_cb.set("선택하여 조건 삽입")
            def insert_condi(event, ctg=ctg, item=item,con_cb=con_cb):
                selection=con_cb.get()
                if isinstance(item,dict):
                    selection=item[selection]
                text.insert(tk.INSERT, f"<{ctg}:{selection}>")
            con_cb.bind("<<ComboboxSelected>>",insert_condi)
            con_cb.pack(fill="x", padx=5, pady=1)
    def update_block():
        for widget in block_container.winfo_children():
            widget.destroy()
        # 태그 설정 & 버튼 생성
        for ctg, items, color in BLOCKS:
            text.tag_configure(ctg, background=color)

            # 카테고리 라벨
            lbl = tk.Label(block_container, text=ctg, bg=color, font=("맑은고딕", 10, "bold"))
            lbl.pack(fill="x", pady=(10,2), padx=2)
            if ctg=="질문/선택지":
                tk.Button(block_container, text="간단한질문생성", font=("맑은고딕", 10, "bold"),command=simple_question).pack(fill="x", padx=5, pady=1)
                tk.Button(block_container, text="표준질문생성", font=("맑은고딕", 10, "bold"),command=advanced_question).pack(fill="x", padx=5, pady=1)
            # 각 아이템 버튼
            for name, token in items:
                btn = tk.Button(
                    block_container,
                    text=name,
                    bg=color,
                    relief="raised",
                    wraplength=200,
                    command=lambda n=name, t=ctg: insert_block(n, t)
                )
                btn.pack(fill="x", padx=5, pady=1)
        update_condi()
    update_block()

    if message:
        text.insert("end", message)

    result = {"text": ""}
    def on_ok():
        result["text"] = text.get("1.0", "end-1c") or ""
        while "[" in result["text"]:
            start_idx=result["text"].index("[")
            end_idx=result["text"].index("]")
            #해당하는 명령어 찾기
            for i in BLOCKS:
                for j in i[1]:
                    Kor_command=remove_bracket(result["text"][start_idx+1:end_idx])
                    issquarebrackets=False
                    if Kor_command.strip()=="중하나를준다":
                        issquarebrackets=True
                        token="<0>"
                    elif Kor_command.strip()=="처음이라면(이)라고말하고,아니면...":
                        token.replace("<-1>",random_alpha_generate())
                    elif remove_bracket(j[0]).strip()==Kor_command.strip():
                        token=j[1]
            read=False; user_input=[];tmp_txt=""
            for al in result["text"][start_idx+1:end_idx]:
                if al=="<":read=True
                elif al==":":tmp_txt=""
                elif al==">":
                    read=False;user_input.append(tmp_txt);tmp_txt=""
                elif read:tmp_txt+=al
            command=extract_between(token,user_input)
            if issquarebrackets: command=f"<{command}>"
            try:
                result["text"]=result["text"][:start_idx]+command+result["text"][end_idx+1:]
            except:
                result["text"]=result["text"][:start_idx]+command+result["text"]
        result["text"]=result["text"].replace("<","[")
        result["text"]=result["text"].replace("<","]")
        dlg.destroy()
    def on_cancel():
        if message:
            result["text"]=message
        else:
            result["text"]=""
        dlg.destroy()
        return

    btn_frame = tk.Frame(dlg)
    btn_frame.pack(side="right", fill="x", pady=5)
    tk.Label(btn_frame,text="뒤 문자열X 블록 : 명령어나 명령어+문자열 조합은 가능합니다").pack(side="left",padx=5)
    tk.Button(btn_frame, text="확인", width=5, command=on_ok).pack(side="left", padx=5)
    tk.Button(btn_frame, text="취소", width=5, command=on_cancel).pack(side="right", padx=5)

    dlg.wait_window()
    return result["text"]
def spriteaction_manager(sprite_img=None, selectoutput=False, isfarmer=False):
    if isfarmer:
        try:
            sprite_img=Image.open(os.path.join(os.getcwd(),"content",f"base병합.png"))
        except:
            messagebox.showerror("알림","base병합 이미지를 불러올 수 없습니다")
            return
    elif not sprite_img:
        try:
            characterID=load_unique_id()
            sprite_img=Image.open(os.path.join(project_dir,"sprites",f"{characterID}.png"))
        except:
            messagebox.showerror("알림","캐릭터 스프라이트 이미지를 불러올 수 없습니다")
            return
    actdlg = tk.Toplevel()
    actdlg.title("스프라이트 액션 관리자")
    actdlg.geometry("500x500")

    if isfarmer:
        anim_data={"농부 액션":list(range(126))}
    else:
        anim_data=load_animation_data() #인덱스 정보 가지고 있는 dict
        data = load_content_json(project_dir)
        entries = data["Changes"]
        for change in entries:
            if change["Target"]=="Data/Characters":
                entries = change["Entries"]
                vals = list(entries.values())[0]
                break;
        gender=vals["Gender"]
        candance=vals.get("FlowerDanceCanDance")
        if isromance():
                            if vals.get("KissSpriteIndex"):
                                anim_data["키스"] = [vals["KissSpriteIndex"]]
                            else:
                                anim_data["키스"] = [28]
                            if candance!=False:
                                if gender=="Female":
                                    anim_data["결혼"] = [36, 37, 38]
                                    anim_data["플라워댄스"] = [40, 41, 42, 43, 44, 45, 46, 47]
                                else:
                                    anim_data["플라워댄스"] = [44, 45, 46, 47]
                                    anim_data["결혼"] = [48, 49, 50, 51]
        elif candance:
                        if gender=="Female":
                            anim_data["플라워댄스"] = [40, 41, 42, 43, 44, 45, 46, 47]
                        else:
                            anim_data["플라워댄스"] = [44, 45, 46, 47]

    scroll_frame = tk.Frame(actdlg)
    scroll_frame.pack(fill="both", expand=True)
    canvas = tk.Canvas(scroll_frame,width=200)
    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="left",fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    # 스크롤 가능한 내부 프레임
    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    # 내부 프레임 사이즈가 바뀌면 캔버스 스크롤 영역 재조정
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    act_canvas_size=(200,400)
    act_canvas = tk.Canvas(scroll_frame, width=act_canvas_size[0], height=act_canvas_size[1])
    act_canvas.pack(side="right",padx=10, pady=10)
    preview_img=sprite_img.crop(sprindex_to_xy(0))
    preview_img = preview_img.resize(act_canvas_size, resample=Image.NEAREST)
    canvas_img = ImageTk.PhotoImage(preview_img)
    act_canvas.create_image(0, 0, anchor="nw", image=canvas_img)
    act_canvas.image = canvas_img
    if selectoutput:
        text_id = act_canvas.create_text(
        10, 10,
        text="",
        width=160,
        anchor="nw",  # 좌상단 기준 위치
        fill="black",
        font=("Arial", 12)
        )

    animation_list=[]

    listbox_dict={} #키:액션이름으로 listbox접근 가능
    selected_listbox=None #삭제 할 때 선택된 리스트박스 판별하기 위함
    def create_listbox(name,frame_list):
        tk.Label(scrollable_frame, text=name, font=("맑은 고딕", 10, "bold")).pack(anchor="w", pady=(10, 0))
        # 리스트 박스 높이: frame_list 길이만큼 (최소 2, 최대 10)
        listbox_height = min(max(len(frame_list), 4), 10)
        listbox = tk.Listbox(scrollable_frame, height=listbox_height)
        listbox_dict[name]=listbox
        
        for frame in frame_list:
            listbox.insert(tk.END, frame)
            # 리스트박스 더블클릭 이벤트
            def on_double_click(event, act_name=name, listbox_ref=listbox):
                if selectoutput:
                    try:
                        action_index=int(''.join(filter(str.isdigit, str(listbox_ref.curselection()))))
                        ref_index=int(listbox_ref.get(listbox_ref.curselection()))
                        animation_list.append([act_name+str(action_index),ref_index])
                        tmp_txt="->".join([key for key,val in animation_list])
                        act_canvas.itemconfig(text_id, text=tmp_txt)
                    except:
                        return
            def on_cb_click(event, listbox_ref=listbox):
                try:
                    ref_index=int(listbox_ref.get(listbox_ref.curselection()))
                    if isfarmer:
                        preview_img=sprite_img.crop(sprindex_to_xy(ref_index,6))
                    else:
                        preview_img=sprite_img.crop(sprindex_to_xy(ref_index))
                    preview_img = preview_img.resize(act_canvas_size, resample=Image.NEAREST)
                    canvas_img = ImageTk.PhotoImage(preview_img)
                    act_canvas.delete("all")
                    if selectoutput:
                        nonlocal text_id
                        text_id = act_canvas.create_text(10, 10, text="->".join([key for key,val in animation_list]),width=160,anchor="nw",fill="black",font=("Arial", 12))
                    act_canvas.create_image(0, 0, anchor="nw", image=canvas_img)
                    act_canvas.image = canvas_img

                    nonlocal selected_listbox
                    selected_listbox=listbox_ref
                except:
                    return
            listbox.bind("<Double-Button-1>", on_double_click)
            listbox.bind("<<ListboxSelect>>", on_cb_click)
            listbox.pack(padx=5, pady=3, fill="x")

    if selectoutput:
        tk.Label(scrollable_frame, text="해당하는 인덱스를 더블클릭하여\n애니메이션을 생성하세요").pack(side="top")
        def undo_handler():
            if animation_list:
                animation_list.pop()
                tmp_txt="->".join([key for key,val in animation_list])
                act_canvas.itemconfig(text_id, text=tmp_txt)
        duration=120
        def preview_handler():
            indexes=[val for key,val in animation_list]
            number=0
            def redraw_canvas():
                nonlocal number
                if number<len(indexes):
                    if isfarmer:
                        preview_img=sprite_img.crop(sprindex_to_xy(indexes[number],6))
                    else:
                        preview_img=sprite_img.crop(sprindex_to_xy(indexes[number]))
                else:
                    return
                preview_img = preview_img.resize(act_canvas_size, resample=Image.NEAREST)
                canvas_img = ImageTk.PhotoImage(preview_img)
                act_canvas.delete("all")
                if selectoutput:
                        nonlocal text_id
                        text_id = act_canvas.create_text(10, 10, text="->".join([key for key,val in animation_list]),width=160,anchor="nw",fill="black",font=("Arial", 12))
                act_canvas.create_image(0, 0, anchor="nw", image=canvas_img)
                act_canvas.image = canvas_img
                number+=1
                act_canvas.after(duration,redraw_canvas)
            redraw_canvas()
        def complete_handler():
            actdlg.destroy()
        ani_btn_frame=tk.Frame(scrollable_frame);ani_btn_frame.pack(side="top")
        undobtn=tk.Button(ani_btn_frame,text="실행취소",command=undo_handler);undobtn.pack(side="left")
        previewbtn=tk.Button(ani_btn_frame,text="미리보기",command=preview_handler);previewbtn.pack(side="left")
        completebtn=tk.Button(ani_btn_frame,text="완료",command=complete_handler);completebtn.pack(side="left")
        tk.Label(scrollable_frame,text="미리보기 프레임 간격").pack(side="top")
        def plus_duration():
            nonlocal duration, drlb
            duration+=10
            drlb.config(text=str(duration))
        def minu_duration():
            nonlocal duration, drlb
            duration=max(duration-10,10)
            drlb.config(text=str(duration))
        preview_frame=tk.Frame(scrollable_frame);preview_frame.pack(side="top")
        tk.Button(preview_frame,text="-",command=minu_duration).pack(side="left")
        drlb=tk.Label(preview_frame,text=str(duration));drlb.pack(side="left")
        tk.Button(preview_frame,text="+",command=plus_duration).pack(side="left")
    else:
        tk.Label(scrollable_frame, text="이 데이터는 모든 스프라이트가\n공유하는 액션 데이터이며,\n존재하는 모든 데이터에 대해\n스프라이트를 가질 필요는 없습니다").pack(side="top")
    if not anim_data: #후에 데이터가 생기면 지워지는 라벨
        tk.Label(scrollable_frame, text="데이터 없음").pack()

    #추가 버튼
    def on_add():
        dlg2 = tk.Toplevel(actdlg)
        dlg2.title("액션 추가")
        dlg2.geometry("300x50")
        tk.Label(dlg2, text="액션이름").grid(row=0, column=0,pady=10)
        name_combo = ttk.Combobox(dlg2, values=list(anim_data.keys()), width=10)
        name_combo.grid(row=0, column=1,pady=10)
        tk.Label(dlg2, text="인덱스").grid(row=0, column=2,pady=10)
        frame_entry = tk.Entry(dlg2,width=5)
        frame_entry.grid(row=0, column=3,pady=10)

        def on_add_by_dlg2():
            act_name = name_combo.get().strip()
            try:
                act_index = int(frame_entry.get())
                if act_index<0:
                    messagebox.showerror("오류", "음수는 불가능합니다")
                    return
            except ValueError:
                messagebox.showerror("오류", "프레임 인덱스는 숫자여야 합니다")
                return
            if act_name:
                for key in list(anim_data.keys()):
                    for i, index in enumerate(list(anim_data[key])):
                        if act_index==index:
                            if key==act_name: #인덱스와 이름이 모두 같은 항목 발견하면
                                messagebox.showinfo("중복","해당 데이터가 이미 존재합니다")
                                return
                            else: #인덱스는 같은데 액션명이 다르면
                                response=messagebox.askyesno("새로운 이름","해당하는 인덱스에 데이터가 이미 존재합니다. 덮어쓰시겠습니까?")
                                if response:
                                    listbox_dict[key].delete(i)
                                    anim_data[key].remove(index)
                                else: return
                if act_name in list(anim_data.keys()):
                    insert_sorted(listbox_dict[act_name],act_index)
                    bisect.insort(anim_data[act_name],act_index)
                else:
                    anim_data[act_name]=[act_index]
                    create_listbox(act_name,[act_index])
                for widget in scrollable_frame.winfo_children():
                    if isinstance(widget,tk.Label) and widget.cget("text")=="데이터 없음":
                        widget.destroy()
                blank_free()
                update_lines()
            else:
                messagebox.showerror("오류", "공백은 불가능합니다")
                return
            dlg2.destroy()
        tk.Button(dlg2, text="추가", command=on_add_by_dlg2).grid(row=0, column=4,pady=10)
    #삭제 버튼
    def on_delete():
        selection=selected_listbox.curselection()
        if selection:
            index_to_delete = int(selected_listbox.get(selection[0]))
            selected_listbox.delete(selection[0])
            for key in list(anim_data.keys()):
                if index_to_delete in anim_data[key]:
                    anim_data[key].remove(index_to_delete)
        else: return
        blank_free()
        update_lines()
    #act_btn_frame=tk.Frame(scrollable_frame).pack(side="top")
    if not isfarmer:
        tk.Button(scrollable_frame, text="추가", command=on_add).pack(side="right")
        tk.Button(scrollable_frame, text="삭제", command=on_delete).pack(side="right")

    # 각 애니메이션 이름별로 Listbox 표시
    for name, frame_list in anim_data.items():
        create_listbox(name,frame_list)
                    
    def update_lines():#lines data 업데이트
        characterID=load_unique_id(data)
        txt_path = os.path.join(os.getcwd(), "content", "user_data","animation_data", f"{characterID}.txt")
        new_lines=""
        for anim_name, indices in anim_data.items():
            indices=sorted(indices)
            for idx_offset, frame_idx in enumerate(indices):
                new_lines+=f"{frame_idx}/{anim_name}/{idx_offset}\n"
                #다시 파일로 저장
        with open(txt_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    def insert_sorted(listbox,item):
        items=list(listbox.get(0,tk.END))
        for idx, existing in enumerate(items):
            if item<existing:
                listbox.insert(idx,item)
                return
        listbox.insert(tk.END,item)
    def blank_free():
        for key in list(anim_data.keys()):
            if not anim_data[key]:
                del anim_data[key]
                listbox_dict[key].destroy()
                for widget in scrollable_frame.winfo_children():
                    if isinstance(widget,tk.Label) and widget.cget("text")==key:
                        widget.destroy()
        if not anim_data: #후에 데이터가 생기면 지워지는 라벨
            tk.Label(scrollable_frame, text="데이터 없음").pack()
    actdlg.wait_window()
    if animation_list:
        return " ".join([str(val) for key,val in animation_list])
    else: return None

#리스트박스 클릭하면 움직이는 미리보기 보여주고 더블클릭하면 애니메이션 키 리턴
def animation_manager(selectoutput=False):
    data=load_content_json(project_dir)
    characterID=load_unique_id(data)
    lowerID=characterID.lower()
    try:
        sprite_img=Image.open(os.path.join(project_dir,"sprites",f"{characterID}.png"))
    except:
        messagebox.showerror("알림","캐릭터 스프라이트 이미지를 불러올 수 없습니다")
        return

    content={
        "Action": "EditData",
        "Target": "Data/animationDescriptions",
        "Entries":  {}
        }
    modifytoindex=is_existing_data(content,data)
    if modifytoindex:
        content=data["Changes"][modifytoindex]
    else:
        response=messagebox.askyesno("수면 애니메이션",f"더욱 풍부한 NPC를 생성하기 위해서는 수면 애니메이션을 정의하면 좋습니다. {lowerID}_sleep을 정의하시겠습니까?\nTIP: 키스 스프라이트로 대체해도 그럴 듯 합니다")
        if response:
            indices=spriteaction_manager(sprite_img,True)
            if indices:
                indices_list=indices.split(" ")
                content["Entries"][lowerID+"_sleep"]=f"{indices_list[0]}/{indices}/{indices_list[-1]}"
    descriptions=content["Entries"]
    def update_lines():
        content["Entries"]=descriptions
        append_to_content(content,data,modifytoindex)
    update_lines()

    actdlg = tk.Toplevel()
    actdlg.title("NPC 애니메이션 관리자")
    actdlg.geometry("500x500")

    scroll_frame = tk.Frame(actdlg)
    scroll_frame.pack(fill="both", expand=True)
    canvas = tk.Canvas(scroll_frame,width=200)
    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="left",fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    # 스크롤 가능한 내부 프레임
    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    # 내부 프레임 사이즈가 바뀌면 캔버스 스크롤 영역 재조정
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    act_canvas_size=(200,400)
    act_canvas = tk.Canvas(scroll_frame, width=act_canvas_size[0], height=act_canvas_size[1])
    act_canvas.pack(side="right",padx=10, pady=10)
    preview_img=sprite_img.crop(sprindex_to_xy(0))
    preview_img = preview_img.resize(act_canvas_size, resample=Image.NEAREST)
    canvas_img = ImageTk.PhotoImage(preview_img)
    act_canvas.create_image(0, 0, anchor="nw", image=canvas_img)
    act_canvas.image = canvas_img

    if selectoutput:
        tk.Label(actdlg,text="항목을 더블클릭하여 애니를 지정하세요").pack(side="top",pady=10)
    listbox_height = 20
    listbox = tk.Listbox(scrollable_frame, height=listbox_height)
        
    for des in list(descriptions.keys()):
        listbox.insert(tk.END, des)
    # 리스트박스 더블클릭 이벤트
    def on_double_click(event):
            if selectoutput:
                try:
                    nonlocal result
                    result=listbox.get(listbox.curselection())
                    actdlg.destroy()
                    
                except:
                    return
    result=""
    def on_cb_click(event):
                try:
                    num=0
                    ani_name=listbox.get(listbox.curselection())
                    indices_list=[]
                    indices=descriptions[ani_name];indices=indices.split("/")
                    for i in range(3):
                        indices[i]=indices[i].split(" ")
                        if i==1:
                            for k in range(3):
                                for j in indices[i]:
                                    indices_list.append(j)
                        else:
                            for j in indices[i]:
                                indices_list.append(j)
                    def canvas_redraw():
                        nonlocal num
                        if num<len(indices_list):
                            preview_img=sprite_img.crop(sprindex_to_xy(int(indices_list[num])))
                        else:
                            return
                        preview_img = preview_img.resize(act_canvas_size, resample=Image.NEAREST)
                        canvas_img = ImageTk.PhotoImage(preview_img)
                        act_canvas.delete("all")
                        act_canvas.create_image(0, 0, anchor="nw", image=canvas_img)
                        act_canvas.image = canvas_img
                        num+=1
                        act_canvas.after(120,canvas_redraw)
                    canvas_redraw()
                except:
                    return
    listbox.bind("<Double-Button-1>", on_double_click)
    listbox.bind("<<ListboxSelect>>", on_cb_click)
    listbox.pack(padx=5, pady=3, fill="x")

    #추가 버튼
    def on_add():
        result=""
        key="key"
        win=tk.Toplevel()
        tk.Label(win,text="제목을 지정해주세요.\n반드시 중복이 아닌, 공백 없는 영문/숫자의 조합이어야 합니다").pack(side="top")
        titleE=tk.Entry(win,width=15);titleE.pack(side="top")
        def offset_handler():
            nonlocal key
            key=titleE.get()
            win.destroy()
        tk.Button(win,text="완료",command=offset_handler).pack(side="top")
        win.wait_window()
        messagebox.showinfo("안내","애니메이션은 진입동작/반복동작/마무리동작으로 이루어져있습니다. 먼저, 진입동작을 만들어 봅시다.")
        indices=spriteaction_manager(sprite_img,True)
        if indices:
            result+=indices
        else: return
        messagebox.showinfo("안내","반복동작을 만들어주세요")
        indices=spriteaction_manager(sprite_img,True)
        if indices:
            result+="/"+indices
        else: return
        messagebox.showinfo("안내","마무리 동작을 만듭시다")
        indices=spriteaction_manager(sprite_img,True)
        if indices:
            result+="/"+indices
        else: return
        offset=""
        shadow=messagebox.askyesno("선택 필드","해당 애니메이션의 그림자를 숨기나요?")
        if shadow: shadow="/laying_down"
        else: shadow=""
        response=messagebox.askyesno("선택 필드","해당 애니메이션에 오프셋을 부여합니까? 캐릭터 이미지가 중심에 맞지 않을때, 그것을 맞추는 역할을 합니다.")
        if response:
            win=tk.Toplevel()
            top_container=tk.Frame(win);top_container.pack()
            tk.Label(top_container,text="X:").pack(side="left")
            xE=tk.Entry(top_container,width=5);xE.pack(side="left")
            tk.Label(top_container,text="Y:").pack(side="left")
            yE=tk.Entry(top_container,width=5);yE.pack(side="left")
            def offset_handler():
                nonlocal offset
                xe=xE.get();ye=yE.get()
                if not xe: xe="0"
                if not ye: ye="0"
                offset=f"/offset {xe} {ye}"
                win.destroy()
            tk.Button(win,text="완료",command=offset_handler).pack(side="top")
            win.wait_window()
        response=messagebox.askyesno("선택 필드","해당 애니메이션에 대사를 지정합니까? 애니메이션을 수행하는 동안, 대화를 걸면 해당 메시지를 반복합니다. Tip: 보통은 [일반 대화창으로 변경] 명령을 이용하여 NPC의 행동을 묘사합니다")
        if response:
            dialcontent={
                "Action": "EditData",
                "Target": "Strings/animationDescriptions",
                "Entries":  {}
                }
            dialindex=is_existing_data(dialcontent,data)
            if dialindex:
                dialcontent=data["Changes"][dialindex]
            dial=open_text_editor()
            if dial:
                dialcontent["Entries"][key]=dial
                append_to_content(dialcontent,data,dialindex)
                result=result+f"/Strings\\animationDescriptions:{key}"+shadow+offset
                descriptions[key]=result
                listbox.insert(tk.END,key)
                update_lines()
            else:
                if shadow or offset:
                    result=result+"/"+shadow+offset
                descriptions[key]=result
                listbox.insert(tk.END,key)
                update_lines()
        else:
            if shadow or offset:
                result=result+"/"+shadow+offset
            descriptions[key]=result
            listbox.insert(tk.END,key)
            update_lines()
    #삭제 버튼
    def on_delete():
        selection=listbox.curselection()
        if selection:
            key_to_delete = listbox.get(selection[0])
            listbox.delete(selection[0])
            for name in list(descriptions.keys()):
                if key_to_delete in descriptions[name]:
                    descriptions[name].remove(key_to_delete)
        else: return
        update_lines()
    tk.Button(scrollable_frame, text="추가", command=on_add).pack(side="right")
    tk.Button(scrollable_frame, text="삭제", command=on_delete).pack(side="right")
    actdlg.wait_window()
    return result
def create_dynamic_input(parent, values=[], side="left",btn_text="입력",res_width=10, isevent=False):
    container = tk.Frame(parent)
    container.pack(side=side, anchor="w", pady=2)
    input_rows = []
    if not isinstance(values, (list,tuple,dict)):
        values=[values]
    length=len(values)

    for i in range(length): #질문이나 이벤트 정보 불러옴
        if values[i]=='q':
            values[i]=[]
            global user_question
            #(name, qid, info)
            question_info=load_response_info()
            for info, qid, name in question_info:
                user_question[name+info]=qid
                values[i].append(name+info)
        elif values[i]=='e':
            values[i]=[]
            global user_event
            event_info=load_event_info()
            for place, name, uid in event_info:
                user_event[name]=uid
                values[i].append(name)
    def add_input():
        row = tk.Frame(container)
        row.pack(side=side, anchor="w", pady=1)
        for j in range(length):
            if isinstance(values[j],dict):
                values[j]=list(values[j].keys())
            is_list=isinstance(values[j],(list,tuple))
            # 입력 위젯: 리스트이면 Combobox, 아니면 Entry
            if is_list:
                max_length=max((len(str(s)) for s in values[j]),default=5)
                widget = ttk.Combobox(row, values=values[j], width=max_length+5)
                if values[j]:
                    widget.current(0)
            elif callable(values[j]):
                res=tk.Entry(row, width=res_width);
                res.pack(side="left",padx=2);res.config(state="readonly")
                def btn_handler():
                        if values[j]==open_text_editor:
                            res_txt=values[j](isevent=isevent)
                        else:
                            try:
                                res_txt=str(values[j]())
                            except:res_txt=values[j]()
                        if not res_txt:
                            return
                        res.config(state="normal")
                        res.delete(0,tk.END)
                        res.insert(0,res_txt)
                        res.config(state="readonly")
                widget=tk.Button(row,text=btn_text,width=5, command=btn_handler)
            else:
                    try:
                        wid=int(values[j])
                        widget = tk.Entry(row, width=wid)
                    except:
                        widget = tk.Label(row, text=values[j])
                
            widget.pack(side="left",padx=2)
        add_btn = tk.Button(row, text="+", width=2, command=add_input)
        add_btn.pack(side="left", padx=2)

        # [-] 버튼 (2개 이상일 때만 표시)
        del_btn = tk.Button(row, text="-", width=2)
        def remove_row():
            row.destroy()
            input_rows.remove(row)
            update_remove_buttons()

        del_btn.config(command=remove_row)
        del_btn.pack(side="left", padx=2)

        comma=tk.Label(row, text=",")
        input_rows.append(row)
        update_remove_buttons()

    def update_remove_buttons():
        # [-] 버튼은 2개 이상일 때만 표시
        for row in input_rows:
            btns = row.winfo_children()
            btns[-3].pack_forget()
            btns[-2].pack_forget()
            btns[-1].pack(side="left", padx=2)
        btn=input_rows[-1].winfo_children()
        btn[-1].pack_forget() #콤마
        if len(input_rows) > 1:
            btn[-3].pack(side="left", padx=2)  # [+]
            btn[-2].pack(side="left", padx=2)  # [-]
        else: 
            btn[-3].pack(side="left", padx=2)  # [+]
    add_input()  # 여러줄 input 받기
    return row
def create_input_box(parent, command, isevent=False, win=None):
    tokens=command.split("/")
    widgets = []
    row=tk.Frame(parent);row.pack(side="top")
    for token in tokens:
        if token[0]=="e":
            try:
                width=int(token[1:])
            except: width=4
            wdg=tk.Entry(row,width=width);wdg.pack(side="left")
            widgets.append(wdg)
        elif token[0]=="c":
            values=parse_input_string(token[2:])
            width = int(token[1:token.index(" ")]) if token[1:token.index(" ")].isdigit() else max((len(s) for s in values),default=5)+5
            wdg=ttk.Combobox(row,values=values,width=width)
            wdg.current(0);wdg.pack(side="left")
            widgets.append(wdg)
        elif token[0]=="f":
            #다중 엔트리 추가 함수 호출
            if isevent:
                side="top"
            else:
                side="left"
            wdg=eval(f"create_dynamic_input(row, {token[2:]},side,'입력',10,isevent)",globals(),locals()) #Frame 안에 위젯들 있는 형태인 점 주의
            widgets.append(wdg)
        elif token[0]=="b":
            width = int(token[1:token.index(" ")]) if token[1:token.index(" ")].isdigit() else 40
            qbox=tk.Entry(row, width=width, state="readonly");qbox.pack(side="left")
            def qadd_handler(cmd=token[token.index(" ")+1:]):
                qbox.config(state="normal")
                if cmd.startswith("open_text"):
                    textd=qbox.get()
                    if textd=="end" or textd=="":
                        textd=open_text_editor(isevent=isevent)
                    else: textd=open_text_editor(message=textd, isevent=isevent)
                else: textd=eval(cmd)
                if textd:
                    qbox.delete(0,tk.END)
                    qbox.insert(0,textd)
                qbox.config(state="readonly")
            qadd=tk.Button(row,text="입력",command=qadd_handler);qadd.pack(side="left")
            widgets.append(qbox)
        elif token[0]=="h":
            if "(" in token:
                function=token[2:]
            else:
                function=f"{token[2:]}()"
            eval(function,globals(),locals()) 
        elif token[0]=="n":
            row=tk.Frame(parent);row.pack(side="top")
        else:
            tk.Label(row,text=token).pack(side="left")
    return widgets
def create_sound_combo(win, parent, tp='b'): #'b'==bgm, 's'=sound
    if tp=='s':
        music_cb=ttk.Combobox(parent,values=list(sound_data.keys()),width=20, state="readonly")
    elif tp=='b':
        music_cb=ttk.Combobox(parent,values=list(music_data.keys()),width=20, state="readonly")
    music_cb.current(0);music_cb.pack(side="left",pady=5,padx=2)
    def on_music_select(event):
        selection=music_cb.get()
        if selection in music_data or selection in sound_data:
            if tp=='b':
                description=music_data[selection][1]
                url=music_data[selection][2]
                show_floating_label(win, description)
            else:
                description=sound_data[selection][1]
                url=None
                show_floating_label(win, description, "#ccffcc")
            if hasattr(on_music_select,"play_btn"):
                on_music_select.play_btn.destroy()
            if url and url.startswith("https:"):
                def play_handler():
                    try: webbrowser.open(url)
                    except:None
                on_music_select.play_btn=tk.Button(parent,text="▶",command=play_handler)
                on_music_select.play_btn.pack(pady=5,side="left")
    music_cb.bind("<<ComboboxSelected>>",on_music_select)
def create_image_combo(win, parent, tp='c'):
    if tp=='c':
        cb=ttk.Combobox(parent,values=list(range(368)),width=10, state="readonly")
        filepath=os.path.join(os.getcwd(),"content","Craftables.png")
        xlen=8
    #elif tp=='b':
        #cb=ttk.Combobox(parent,values=list(range(236)),width=20, state="readonly")
        #filepath=os.path.join(os.getcwd(),"content","base병합.png")
        #xlen=6
    cb.current(0);cb.pack(side="left",pady=5,padx=2)
    img=Image.open(filepath)
    def on_select(event):
        selection=cb.get()
        preview_img=img.crop(sprindex_to_xy(selection,xlen))
        preview_img = preview_img.resize((50,100), resample=Image.NEAREST)
        show_floating_label(win, preview_img)
    cb.bind("<<ComboboxSelected>>",on_select)
def create_event_combo(parent, tp='e'):
    values=[]
    if tp=='q':
        global user_question
        #(name, qid, info)
        question_info=load_response_info()
        for info, qid, name in question_info:
            user_question[name+info]=qid
            values.append(name+info)
    elif tp=='e':
        global user_event
        info=load_event_info()
        for place, name, uid in info:
            user_event[name]=uid
            values.append(name)
    cb=ttk.Combobox(parent,values=values,width=20, state="readonly")
    if values:
        cb.current(0)
    cb.pack(side="left",pady=5,padx=2)

def parse_input_string(s, local_vars=None):
    s = s.strip()
    if local_vars is None:
        local_vars = globals()

    # 1. 문자열 리터럴만 있는 경우 (예: 'q')
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        return s[1:-1]

    # 2. 전체 리스트 시도 (예: '[5]', '[a, b]', '[range(3)]', "['cat','dog']")
    if s.startswith("[") and s.endswith("]"):
        content = s[1:-1].strip()

        # 먼저, 리터럴로 파싱 시도
        try:
            return ast.literal_eval(s)
        except:
            pass

        # 수동 파싱
        items = [item.strip() for item in content.split(",")]
        result = []
        for item in items:
            # range() 처리
            if item.startswith("range("):
                try:
                    val = eval(item, {}, {})  # 안전한 범위 평가
                    result.append(list(val))
                    continue
                except:
                    result.append(item)
                    continue

            # 변수 접근
            if item in local_vars:
                val = local_vars[item]
                if isinstance(val, dict):
                    result.append(list(val.keys()))
                elif isinstance(val, list):
                    result.append(val)
                else:
                    result.append(val)
            else:
                result.append(item)
        return result

    # 3. 변수 하나만 있는 경우 (예: DayOfWeek)
    if s in local_vars:
        val = local_vars[s]
        if isinstance(val, dict):
            return list(val.keys())
        elif isinstance(val, list):
            return val
        else:
            return val

    # 4. 리터럴 단일 값 (숫자, 문자열 리스트 등)
    try:
        return ast.literal_eval(s)
    except:
        return s #유저 입력을 위한 것이므로 key만 접근함
def find_matching_bracket(token, start_idx,str="[]"):
    """
    시작 인덱스(start_idx)는 반드시 '['를 가리켜야 한다고 가정.
    해당 여는 괄호에 대응되는 닫는 괄호 위치를 반환.
    """
    if token[start_idx] != str[0]:
        raise ValueError("start_idx가 여는 괄호를 가리켜야 합니다.")
    depth = 0
    for i in range(start_idx, len(token)):
        if token[i] == str[0]:
            depth += 1
        elif token[i] == str[1]:
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("짝이 맞는 닫는 괄호를 찾을 수 없습니다.")
def find_token_start(token):
    match = re.search(r"<\d+", token)
    if match:
        start_idx = match.start()
        end_idx = find_matching_bracket(token,start_idx,"<>")
        return (start_idx, end_idx)
    match = re.search(r"\[\d+", token)
    if match:
        start_idx = match.start()
        end_idx = find_matching_bracket(token,start_idx)
        return (start_idx, end_idx)
    return -1  # 찾지 못했을 때
def count_and_max_index_from_tokens(tokens):
    token_count = 0
    max_index = -1

    for tok in tokens:
        # 모든 대괄호나 꺾쇠괄호 내부의 정수 추출
        # 예: [0], [0:dict.key], <1:sd_items.id> 등
        matches = re.findall(r"[<\[](\d+)", tok)
        if matches:
            token_count += 1
            for m in matches:
                try:
                    idx = int(m)
                    if idx > max_index:
                        max_index = idx
                except ValueError:
                    continue

    return token_count, max_index
def extract_between(token,user_input, offset=0):
    while bool(re.search(r"\[\d+",token)) or bool(re.search(r"\<\d+",token)): 
        start_idx, end_idx=find_token_start(token)

        if token[start_idx]=="<":coffset=0
        else:coffset=offset

        expr=token[start_idx+1:end_idx]
        if ":" in expr:
            idx=int(expr[:expr.index(":")])
            expr=expr[expr.index(":")+1:]
            if "]" in expr:
                si=expr.index("[");ei=expr.index("]");one=expr[:si]
                two=expr[si+1:ei]
                if two.isdigit():
                    two=f"[{two}]"
                else:two="[\""+two+"\"]"
            elif "." in expr:
                si=expr.index(".");one=expr[:si];two=expr[si:]
            else:
                one=expr;two=""
            key = "[\""+user_input[idx+coffset]+"\"]"
            try:
                value=eval(one+key+two)
                if type(value)==int:
                    value=str(value)
                if value:
                    token=token.replace(token[start_idx:end_idx+1], value)
                elif value=="":
                    try:
                        token=token[:start_idx]+token[end_idx+1:]
                    except:
                        token=token[:start_idx]
            except Exception as e:
                return None
        elif "~" in expr:
            #물결표가 나올때는 :나 다른 특수기호와 혼합할 수 없으며, 마지막에만 쓸 수 있음 예시 <2~> : 2부터의 인덱스를 모두 튜플로 만듬
            idx=int(expr[:expr.index("~")])
            token=token.replace(token[start_idx:end_idx+1],"("+(",".join([f"'{s}'" for s in eval("user_input[idx:]",locals())]))+")")
            break;
        else:
            idx=int(expr)
            token=token.replace(token[start_idx:end_idx+1],user_input[idx+coffset])
    result=token.split("_")
    for i in range(len(result)):
        if re.search(r'[a-zA-Z]',result[i]):
            try:
                result=eval(token,globals())
            except: return token
            return result
        try:
            result[i]=eval(result[i],globals())
        #수식이 써지는지 확인
        except: continue
    for i in range(len(result)):
        if type(result[i])!=str:
            result[i]=str(result[i])
    return "_".join(result)
def parse_pattern_repeated(tokens: list, user_input: list):
    result = []
    token_len, index_len=count_and_max_index_from_tokens(tokens)
    current_idx=0;cursor=0;untoken=0
    #user_input    token의 커서 
    while token_len and current_idx<len(user_input)//(index_len+1)*token_len:
        istok=False
        try:
            if ("<" in tokens[cursor]) or ("[" in tokens[cursor]):
                istok=True
                value = extract_between(tokens[cursor], user_input, offset=(current_idx//token_len)*(index_len+1))
            elif "(" in tokens[cursor]:
                value=eval(tokens[cursor],globals())
            else: value=tokens[cursor]
        except:
            value=tokens[cursor]
        if not value: return None
        if istok:
            if type(value)==int:
                result.append(str(value))
            else: result.append(value)
            current_idx+=1
        #첫번째 순회에서만 명령어 삽입
        elif not (current_idx//token_len)*(index_len+1):
            try: result.append(str(value))
            except: result.append(value)
            untoken+=1
        if "~"in tokens[cursor]:
                break;
        cursor+=1
        cursor=max([cursor%(token_len+untoken),untoken])
    if not token_len:
        return tokens
    else:
        further=[]
        for tok in tokens[::-1]:
            if "<" in tok or "[" in tok:
                break;
            else:
                further.append(tok)
        further.reverse()
        return result+further
    return result
def parse_input_string_tokens(line: str, user_input: list):
    tokens = line.split()
    result= parse_pattern_repeated(tokens, user_input)
    if result:
        return result
    else:
        return None

def show_floating_label(parent, text, color="#ffffcc"):
    float_win = tk.Toplevel(parent)
    alpha=0.9
    float_win.overrideredirect(True)  # 타이틀바 제거
    float_win.attributes("-topmost", True)
    float_win.attributes("-alpha", alpha)  # 반투명
    float_win.configure(bg=color)
    if isinstance(text,str):
        label = tk.Label(float_win, text=text, bg=color, fg="black", font=("맑은 고딕", 10))
    else:
        image=ImageTk.PhotoImage(text)
        label = tk.Label(float_win, image=image)
        label.image=image
    label.pack(ipadx=10, ipady=5)

    # 위치를 부모 윈도우 중앙 근처로 이동
    x = parent.winfo_rootx() + 100+random.randrange(-150,150)
    y = parent.winfo_rooty() + 50+random.randrange(-150,150)
    float_win.geometry(f"+{x}+{y}")

    def adjust_alpha():
        nonlocal alpha
        if 0.8<alpha<=0.9:
            alpha-=0.01
        else:
            alpha-=0.1
        if alpha<=0:
            float_win.destroy()
        try:
            float_win.attributes("-alpha", alpha)
        except:
            return
        parent.after(100, adjust_alpha)
    parent.after(100, adjust_alpha)
    #이벤트 장소, 이름, 아이디 리턴, 이벤트 txt 수정도
def open_event_editor(isfork=False):
    data=load_content_json(project_dir)
    win = tk.Toplevel()
    if not isfork:
        win.title("이벤트 추가")
    else:
        win.title("포크가 참일 때 이어지는 스크립트 추가")
    win.geometry("1200x600")

    # ── 상단 입력부: 장소 선택, 이벤트 이름 입력, 저장 버튼 ──
    top_frame = tk.Frame(win)
    top_frame.pack(fill="x", pady=10)
    if not isfork:
        tk.Label(top_frame, text="장소:").pack(side="left", padx=(10, 5))
    else:
        tk.Label(top_frame, text="★장소:").pack(side="left", padx=(10, 5))
    location_cb = ttk.Combobox(top_frame, values=location_name, width=15)
    #새 위치 항목이 들어온다면 유저의 이벤트 스크립트를 event 항목에 추가해야함
    location_cb.current(0)
    location_cb.pack(side="left", padx=5)
    if not isfork:
        tk.Label(top_frame, text="이벤트 이름(한글 가능):").pack(side="left", padx=5)
    else:
        tk.Label(top_frame, text="이벤트 이름(★공백없는 영문/숫자의 조합):").pack(side="left", padx=5)
    event_name_entry = tk.Entry(top_frame, width=20)
    event_name_entry.pack(side="left", padx=5)

    eventName=""
    def save_handler():
        nonlocal eventName
        event_location=location_cb.get()
        eventName=event_name_entry.get().strip()
        event_script=""
        if not eventName:
            messagebox.showerror("오류","공백 제목은 불가능합니다")
            return
        #저장하기
        if not isfork:
            eventID=str(random_number_generate(7,Invalid_eventID))
            for eventID in list(user_event.values()):
                eventID=str(random_number_generate(7,Invalid_eventID))
            if not condition_input_save:
                messagebox.showerror("오류","전제 조건이 없습니다")
                return
            eventKey=eventID+"".join(list(condition_input_save.values()))
            #for cd in list(condition_input_save.values()):
                #eventKey+="/"+cd
            #앞의 세 필드, try 처리 해야함
            try:
                for widget in music_container.winfo_children():
                    if isinstance(widget,ttk.Combobox):
                        event_script+=music_data[widget.get()][0]
                event_script+=f"/{basic_field2[0]} {basic_field2[1]}/"
                basic_field3=[]
                for widget in basic_npc_container.winfo_children():
                    if isinstance(widget,tk.Frame):
                        for wdg in widget.winfo_children():
                            if isinstance(wdg,tk.Frame):
                                for wg in wdg.winfo_children():
                                    if isinstance(wg,ttk.Combobox) and wg not in basic_field3:
                                        basic_field3.append(wg)
                                    if isinstance(wg,tk.Entry) and wg not in basic_field3:
                                        basic_field3.append(wg)
                #farmer 23 22 0
                basic_text3=[]
                for i in range(0,len(basic_field3),2):
                    basic_text3.append(basic_field3[i].get()+" "+" ".join(re.findall(r'\b\d+\b', basic_field3[i+1].get())))
                event_script+=" ".join(basic_text3)
            except:
                messagebox.showerror("오류","초기 세 필드 중 무언가 잘못된 값이 입력되었습니다")
                return
        else:
            eventKey=eventName
        for block in user_script:
            event_script+="/"+block[1]
        while event_script.find("/(breakEND)")!=-1:
            try:
                event_script=event_script.replace("/(break)","(break)")
                breakindex=event_script.index("(break)")+7
                endindex=event_script.index("/(breakEND)")
                event_script=event_script[:breakindex]+event_script[breakindex:endindex].replace("/","\\")+"/pause 1000"+event_script[endindex+11:]
                break;
            except:
                messagebox.showerror("오류","quickQuestion 반응이 존재하지 않습니다")
                return
        if isfork:
            if event_script[0]=="/":
                event_script=event_script[1:]

        #content에 이벤트 저장
        if event_location in location_name:
            content={
                "Action": "EditData",
                "Target": f"Data/Events/{event_location}",
                "Entries": {}
            }
        else:
            content={
                "Action": "Load",
                "Target": f"Data/Events/{event_location}",
                "Entries": {}
            }
        data=load_content_json(project_dir)
        modifytoindex=is_existing_data(content,data)
        if modifytoindex:
            content=data["Changes"][modifytoindex]
        content["Entries"][eventKey]=event_script
        append_to_content(content,data,modifytoindex)

        if not isfork:
            new_lines=""
            info=load_event_info(data)
            info.append((event_location,eventName,eventID))
            for lc, nm, eid in info:
                new_lines+=f"{lc}/{nm}/{eid}\n"
            characterID=load_unique_id(data)
            with open(os.path.join("content", "user_data","event_data", f"{characterID}.txt"), "w", encoding="utf-8") as f:
                f.writelines(new_lines) #이벤트 관리 메모장에 업데이트

        win.destroy()
    save_btn = tk.Button(top_frame, text="저장하고 닫기",command=save_handler)
    save_btn.pack(side="left", padx=10)

    # ── 본문: 좌(전제조건), 우(이벤트 블록) ──
    body = tk.Frame(win)
    body.pack(fill="both", expand=True)
    if not isfork:
        # 왼쪽0: 조건 필드
        condition_frame = tk.LabelFrame(body, text="전제조건", padx=10, pady=10)
        condition_frame.pack(side="left", fill="y", padx=10, pady=5)

        condition_input_save={} #일시적으로 유저가 설정한 조건명과 내용을 기억함
        with open(os.path.join(os.getcwd(), "content","event_preconditions.json"), encoding="utf-8") as f:
            condition_data=json.load(f)
        def add_condition():
            win2 = tk.Toplevel(win)
            win2.title("이벤트 실행 조건")
            win2.geometry("800x200")
            cbcontainer=tk.Frame(win2)
            cbcontainer.pack(side="top")
            cdcombo=ttk.Combobox(cbcontainer,values=list(condition_data.keys()),width=5,state="readonly")
            cdcombo.pack(side="left");cdcombo.set("선택")

            def on_category_change(event):
                for widget in win2.winfo_children():
                    if widget!=cbcontainer:
                        widget.destroy()
                for widget in cbcontainer.winfo_children():
                    if widget!=cdcombo:
                        widget.destroy()
                category=cdcombo.get()
                displayed_vals=list(condition_data[category].keys())
                displayed_val=[] #split한 정보 기억
                code_list=[]
                description_list=[]
                for i,val in enumerate(displayed_vals):
                    displayed_val.append(val.split("/"))
                    code_list.append(condition_data[category][val][0])
                    description_list.append(condition_data[category][val][1])
                    displayed_vals[i]=""
                    for v in displayed_val[i]:
                        if not (v[0]=="e" or v[0]=="c" or v[0]=="f"):
                            displayed_vals[i]+=v #라벨 정보들만 저장해서 표시
                dtcombo=ttk.Combobox(cbcontainer,values=displayed_vals,width=30,state="readonly")
                dtcombo.pack(side="right");dtcombo.set("선택")
                def on_token_change(event):
                    for widget in win2.winfo_children():
                        if widget!=cbcontainer:
                            widget.destroy()
                    index=displayed_vals.index(dtcombo.get())
                    tokens=displayed_val[index]
                    description=description_list[index]
                    code=code_list[index]
                    add_selection_box(win2,tokens,code,description)
                dtcombo.bind("<<ComboboxSelected>>",on_token_change)
            cdcombo.bind("<<ComboboxSelected>>",on_category_change)
        def add_selection_box(win2,tokens,code,description,user_input=None):
            row=tk.Frame(win2);row.pack(pady=30)
            #if user_input:
                #index=1 #유저 인풋에 따라 배치 고민해보기,
                #불러오기를 할 때 다중 엔트리 기억에서 문제생김
                #response=messagebox.askokcancel("잠깐!!","해당 조건을 다시 입력하시겠습니까? 확인을 눌러도 저장 전까지는 이전 데이터가 그대로 보존됩니다.")
                #if response:
                    #return
            for token in tokens:
                if token[0]=="e":
                    tk.Entry(row,width=4).pack(side="left")
                elif token[0]=="c":
                    tkcb=ttk.Combobox(row,values=parse_input_string(token[2:]),width=10)
                    tkcb.current(0);tkcb.pack(side="left")
                elif token[0]=="f":
                    #다중 엔트리 추가 함수 호출
                    create_dynamic_input(row, parse_input_string(token[2:]))
                else:
                    tk.Label(row,text=token).pack(side="left")
            token_bool=ttk.Combobox(row,values=['이다','이 아니다'],width=10,state="readonly")
            token_bool.current(0);token_bool.pack(side="left")

            def add_handler():
                user_input=[]
                for widget in row.winfo_children():
                    if isinstance(widget,(ttk.Combobox,tk.Entry)):
                        user_input.append(widget.get())
                    elif isinstance(widget,tk.Frame):
                        for wg in widget.winfo_children():
                            if isinstance(wg,tk.Frame):
                                for weg in wg.winfo_children():
                                    if isinstance(weg,(ttk.Combobox,tk.Entry)):
                                        user_input.append(weg.get())
                for tok in user_input:
                    if not tok:
                        messagebox.showerror("오류","공백은 불가합니다")
                        return
                output_code=parse_input_string_tokens(code, user_input[:-1])
                if output_code: output_code=' '.join(output_code)
                else:
                    messagebox.showerror("오류","유효하지 않은 값입니다")
                    return
                if user_input[-1]=="이 아니다":
                    output_code='/!'+output_code[1:]
                current_title=cd_title.get()
                if current_title in condition_input_save.keys():
                    messagebox.showerror("오류","동일한 제목의 조건이 이미 존재합니다")
                    return
                condition_input_save[current_title]=output_code
                #불러오기 미구현
                cd_btn_frame=tk.Frame(condition_frame);cd_btn_frame.pack(side="top")
                cd_adj_btn=tk.Button(cd_btn_frame, text=current_title, state=tk.DISABLED, command=lambda tk=tokens, cd=code, ds=description, ip=user_input: add_selection_box(win2,tk,cd,ds,ip))
                cd_adj_btn.pack(side="left")
                def delete_condition():
                    del condition_input_save[current_title]
                    cd_adj_btn.destroy()
                    des_btn.destroy()
                des_btn=tk.Button(cd_btn_frame, text="X", command=delete_condition)
                des_btn.pack(side="right")
                messagebox.showinfo("완료","조건이 추가되었습니다\n※삭제/수정/불러오기 기능이 구현되지 않았으니 주의!")
            addFrame=tk.Frame(win2);addFrame.pack(side="bottom",pady=10)

            add_btn=tk.Button(addFrame,text="추가",command=add_handler).pack(side="right")
            cd_title=tk.Entry(addFrame,width=10);cd_title.pack(side="left");
            def set_auto_title(i):
                output="조건"+str(i)
                if output in condition_input_save.keys():
                    return set_auto_title(i+1)
                else:
                    return output
            cd_title.insert(0, set_auto_title(0))
            tk.Label(win2, text=description).pack(side="bottom")

        tk.Button(condition_frame, text="+ 조건 추가",command=add_condition).pack(side="top",pady=5)
        #버튼 누르면 필드 종류 콤보박스 선택해서 선택

    # 왼쪽1: 스크립트 조립 칸
    script_frame = tk.LabelFrame(body, text="이벤트 스크립트", padx=10, pady=10)
    script_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

    # 스크립트 캔버스 (스크롤 포함)
    canvas_container = tk.Frame(script_frame)
    canvas_container.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_container, bg="#f0f0f0")
    scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    script_area = tk.Frame(canvas, bg="#f0f0f0")
    canvas.create_window((0, 0), window=script_area, anchor="nw")
    def update_script_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    script_area.bind("<Configure>", update_script_scroll)

    #이벤트 스크립트 기본 항목
    if not isfork:
        music_container=tk.Frame(script_area);music_container.pack(side="top",pady=5)
        tk.Label(music_container,text="BGM : ").pack(side="left",pady=5,padx=2)
        create_sound_combo(win, music_container, tp='b')
        basic_field2=(20,40);location_lb=tk.Label(music_container,
                                              text="              ("+str(basic_field2[0])+","+str(basic_field2[1])+")")
        def camera_handler():
            try:
                _,x,y,_=select_location(location_cb.get(),False,isdirection=False)
                nonlocal basic_field2;basic_field2=(x,y)
                location_lb.config(text="              ("+str(basic_field2[0])+","+str(basic_field2[1])+")")
            except:
                return
        camera_adjust_btn=tk.Button(music_container, text="카메라", command=camera_handler)
        camera_adjust_btn.pack(side="right", pady=10)
        location_lb.pack(side="right",pady=5)
        basic_npc_container=tk.Frame(script_area);basic_npc_container.pack(side="top")
        tk.Label(basic_npc_container,text="캐릭터 초기 위치").pack(side="top")
        create_dynamic_input(basic_npc_container, values=[NPCName+["farmer"],lambda: select_location(location_cb.get(),numdirection=True)],side="top",btn_text="위치")

    # 기본 상태로는 블록 없음
    blanklb=tk.Label(script_area, text="여기에 블록이 추가됩니다");blanklb.pack(pady=10)
    def update_script_block():
        if not isfork:
            for widget in script_area.winfo_children():
                if widget not in [music_container,basic_npc_container]:
                    widget.destroy()
        else:
            for widget in script_area.winfo_children():
                widget.destroy()
        for i in range(len(user_script)):
            #preview_txt,output_code,color
            item=user_script[i]
            block = tk.Frame(script_area, bd=2, bg=item[2], relief="groove", padx=20, pady=5)
            block.pack(fill="x",pady=3, padx=3,side="top")

            def up_btn(index):
                if index>0:
                    user_script[index],user_script[index-1]=user_script[index-1],user_script[index]
                    update_script_block()
            def down_btn(index):
                if index<len(user_script)-1:
                    user_script[index],user_script[index+1]=user_script[index+1],user_script[index]
                    update_script_block()
            def block_destroy(index):
                for i in range(index+1,len(user_script)):
                    up_btn(i)
                user_script.pop()
                update_script_block()
            block_top=tk.Frame(block,bg=item[2]);block_top.pack(fill="x",side="top")
            tk.Button(block_top,text="△",command=partial(up_btn, i)).pack(side="left")
            tk.Button(block_top,text="▽",command=partial(down_btn, i)).pack(side="left")
            tk.Button(block_top,text="X",command=partial(block_destroy, i)).pack(side="right")
            
            tk.Label(block,text=item[0],wraplength=450,width=60,bg=item[2]).pack(side="top")
        

    #─────오른쪽: 스크립트 블록──────────────────
    block_frame = tk.LabelFrame(body, text="블록",padx=10, pady=10)
    block_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    block_controls = tk.Frame(block_frame)
    block_controls.pack(fill="x", pady=5)

    # 스크립트 캔버스 (스크롤 포함)
    block_canvas_container = tk.Frame(block_frame)
    block_canvas_container.pack(fill="both", expand=True)

    block_canvas = tk.Canvas(block_canvas_container, bg="#f0f0f0")
    block_scrollbar = tk.Scrollbar(block_canvas_container, orient="vertical", command=block_canvas.yview)
    block_canvas.configure(yscrollcommand=block_scrollbar.set)

    block_scrollbar.pack(side="right", fill="y")
    block_canvas.pack(side="left", fill="both", expand=True)

    block_area = tk.Frame(block_canvas, bg="#f0f0f0")
    block_canvas.create_window((0, 0), window=block_area, anchor="nw")
    def update_block_scroll(event):
        block_canvas.configure(scrollregion=block_canvas.bbox("all"))
    block_area.bind("<Configure>", update_block_scroll)

    with open(os.path.join(os.getcwd(), "content","event_script_block.json"), encoding="utf-8") as f:
            block_data=json.load(f)
    style = ttk.Style()
    style.configure("Custom.TCombobox",font=("Helvetica", 14),padding=5)
    block_ctcb=ttk.Combobox(block_area,values=list(block_data.keys()),state="readonly",style="Custom.TCombobox")
    block_ctcb.pack(fill="x",pady=3,side="top");block_ctcb.current(0)
    block_ctcb.configure(justify='center')  # Entry 기본 정렬

    user_script=[] #블럭을 순서대로 저장함
    def add_block(color,item,command):
        block = tk.Frame(block_area, bd=2, bg=color, relief="groove", padx=5, pady=5)
        block.pack(fill="x", pady=3, padx=3,side="top")
        block_top=tk.Frame(block,bg=color);block_top.pack(fill="x",side="top")
        def add_script():
            user_input_box=[]
            user_input=[]
            for row in block.winfo_children():
                if isinstance(row,tk.Frame):
                    for widget in row.winfo_children():
                        if isinstance(widget,tk.Entry):
                            if widget not in user_input_box:
                                user_input_box.append(widget)
                        if isinstance(widget,ttk.Combobox):
                            if widget not in user_input_box:
                                user_input_box.append(widget)
                        if isinstance(widget,tk.Frame):
                            for wdg in widget.winfo_children():
                                if isinstance(wdg,tk.Entry):
                                    if wdg not in user_input_box:
                                        user_input_box.append(wdg)
                                if isinstance(wdg,ttk.Combobox):
                                    if wdg not in user_input_box:
                                        user_input_box.append(wdg)
                                if isinstance(wdg,tk.Frame):
                                    for wg in wdg.winfo_children():
                                        if isinstance(wg,tk.Entry):
                                            if wg not in user_input_box:
                                                user_input_box.append(wg)
                                        if isinstance(wg,ttk.Combobox):
                                            if wg not in user_input_box:
                                                user_input_box.append(wg)
            for widget in user_input_box:
                user_input.append(widget.get())
            try:
                output_code=" ".join(parse_input_string_tokens(command,user_input))
            except:
                messagebox.showerror("오류","유효하지 않은 요청입니다")
                return

            preview_txt=""
            blocksplit=item.split("/")
            point=0
            for i in range(len(blocksplit)):
                if blocksplit[i][0] in ["e","c","b","h"]:
                    preview_txt+=user_input[point]+" "
                    point+=1
                elif blocksplit[i][0]=="n":
                    preview_txt+="\n"
                elif blocksplit[i][0]=="f":
                    preview_txt+="\n"+" ".join(user_input[point:])+"\n"
                else:
                    preview_txt+=blocksplit[i]

            nonlocal user_script
            user_script.append([preview_txt,output_code,color])
            update_script_block()
        tk.Button(block_top,text="블록+",command=add_script).pack(side="left")
        create_input_box(block, item, True, win)
    def block_ctcb_selected(event):
        for widget in block_area.winfo_children():
            if widget!=block_ctcb:
                widget.destroy()
        selected=block_ctcb.get()
        if selected in block_data:
            for item,command in block_data[selected][1].items():
                add_block(block_data[selected][0],item,command)
    block_ctcb.bind("<<ComboboxSelected>>",block_ctcb_selected)

    #block_ctcb_selected()
    #for k,v in block_data.items():
        #tk.Label(block_area,text=k).pack(side="top")
        #for item,command in v[1].items():
            #add_block(v[0],item,command)

    win.wait_window()
    try: return eventName
    except: return None


    #_______________________________________

#______________________기본 정보 폼____________________________________________
row = 0
form_frame = tk.Frame(root)
menu_fields = [
    ("성별", {"여성":"Female","남성":"Male","미정":"Undefined"}),
    ("나이", {"어린이":"Child","청소년":"Teen","성인":"Adult"}),
    ("공손함", {"중립":"Neutral","공손":"Polite","무례":"Rude"}),
    ("사교성", {"중립":"Neutral","사교적":"Outgoing","내성적":"Shy"}),
    ("낙관성", {"중립":"Neutral","부정적":"Negative","긍정적":"Positive"}),
    ("태어난 계절", {"봄":"spring","여름":"summer","가을":"fall","겨울":"winter"}),
    ("거주 지역", {"타운":"Town","해변":"Beach","숲":"Forest","사막":"Desert","그 외":"Other"}),
    ("어두운 피부 여부", {"아니오":False,"예":True}),
]
vars_map = {}
for label, mapping in menu_fields:
    tk.Label(form_frame, text=label).grid(row=row, column=0, sticky="w")
    var = tk.StringVar(form_frame)
    var.set(list(mapping.keys())[0])
    tk.OptionMenu(form_frame, var, *mapping.keys()).grid(row=row, column=1, sticky="w")
    vars_map[label] = (var, mapping)
    row += 1
# 생일
tk.Label(form_frame, text="태어난 날 (1~28)").grid(row=row, column=0, sticky="w")
birthday_var = tk.IntVar(form_frame)
birthday_var.set(1)
tk.Spinbox(form_frame, from_=1, to=28, textvariable=birthday_var, width=5).grid(row=row, column=1, sticky="w")
row += 1
# 연애 가능 여부
romance_var = tk.BooleanVar(form_frame)
romance_var.set(False)  # 기본값은 False
tk.Checkbutton(form_frame, text="연애 가능", variable=romance_var).grid(row=row, column=0, columnspan=2, sticky="w")
row += 1
status_lbl = tk.Label(form_frame, text="", anchor="w")
# 초기 출현 위치 정보를 임시로 보관할 전역 변수
home_entry = {
                    "Id": "Default",
                    "Condition": None,
                    "Location": "Town",
                    "Tile": { "X": 20, "Y": 40 },
                    "Direction": "down"
                }
# “초기 위치 선택” 핸들러
def on_pick_home():
    global home_entry
    vals = select_location()
    if not vals:
        return
    m, x, y, d = vals
    home_entry = {
        "Id":"Default", "Condition":None,
        "Location":m, "Tile":{"X":x,"Y":y}, "Direction":d
    }
    #미리보기
    status_lbl.config(text=f"초기 위치: {m}({x},{y}) facing {d}")
tk.Button(form_frame, text="초기 위치 선택", command=on_pick_home) \
    .grid(row=row, column=0, columnspan=2, pady=10)
row+=1
status_lbl.grid(row=row, column=0, columnspan=2, sticky="w", pady=10)
row+=1
# “다음” 버튼 핸들러
def on_form_next():
    name = entry_name.get().strip()
    values = {
        "BirthDay": birthday_var.get(),
        "CanBeRomanced": romance_var.get()
    }
    # vars_map 으로부터 나머지 값 매핑
    key_map = {
        "성별":"Gender","나이":"Age","공손함":"Manner","사교성":"SocialAnxiety",
        "낙관성":"Optimism","태어난 계절":"BirthSeason","거주 지역":"HomeRegion",
        "어두운 피부 여부":"IsDarkSkinned"
    }
    for label, (var, mapping) in vars_map.items():
        values[key_map[label]] = mapping[var.get()]

    
    values["Home"] = [home_entry]

    # 프로젝트 생성
    proj = create_project_folder(name, values)
    global project_dir
    project_dir = proj

    form_frame.pack_forget()
    open_advanced_form()
tk.Button(form_frame, text="다음", command=on_form_next) \
    .grid(row=row, column=0, columnspan=2, pady=10)
form_frame.pack_forget()

def img_combined(img1, img2, vertical=True):
    if (vertical==False):
        new_width = img1.width + img2.width
        new_height = max(img1.height, img2.height)
        pastex=img1.width 
        pastey=0
    else:
        new_width = max(img1.width, img2.width)
        new_height = img1.height + img2.height
        pastex=0
        pastey=img1.height
    combined = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    combined.paste(img1, (0, 0))               
    combined.paste(img2, (pastex, pastey))
    return combined
def blend_colors(bg, fg):
    alpha = fg[3] / 255
    r = int(fg[0] * alpha + bg[0] * (1 - alpha))
    g = int(fg[1] * alpha + bg[1] * (1 - alpha))
    b = int(fg[2] * alpha + bg[2] * (1 - alpha))
    a = max(bg[3], fg[3])  # 결과 알파는 두 알파 중 더 큰 값으로 (선택 가능)
    return (r, g, b, a)
def replace_color(originimg, target_color, replacement_color,skincolors=None):
    img=originimg.copy()
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixels[x, y] == target_color:
                if len(replacement_color)>=4 and (replacement_color[3]<255) and skincolors:
                    if target_color==(142,31,12,255):new_color=skincolors[2] #여기다가 합성해야함
                    elif target_color==(112,23,24,255):new_color=skincolors[1]
                    elif target_color==(74,12,6,255):new_color=skincolors[0]
                    else: new_color = skincolors[2]
                    pixels[x,y]=blend_colors(pixels[x,y],new_color)
                else: pixels[x, y] = replacement_color
    return img
def sprindex_to_xy(index, xlen=4):
    #index=(row,col) tuple
    if type(index)==str:
        index=int(index)
    try:
        row=index[0]
        col=index[1]
    except:
        row=index//xlen
        col=index%xlen
    return (16*col,32*row,16*col+16,32*row+32)
def erase_region(img, box): #박스에는 row,col/x1 y1 x2 y2 또는 그냥 숫자 형식 모두 허용
    try:
        if len(box)<4:
            box=sprindex_to_xy(box)
    except:
        box=(box//4,box%4) #row, col
        box=sprindex_to_xy(box)
    if img.mode!="RGBA":
        img=img.convert("RGBA")
    pixels=img.load()
    x1,y1,x2,y2=box
    for x in range(x1,x2):
        for y in range(y1,y2):
            pixels[x,y]=(0,0,0,0)
    return img
def isinsprite(dictt, index, erase=False): #입력된 dict further_act만 지움(results는 따로 컨트롤)
    try:
        index=sprindex_to_xy(index) #x1 y1 x2 y2
    except:
        index=(index//4,index%4) #row, col
        index=sprindex_to_xy(index)
    result=False
    for k,v in dictt.items():
        for token in v:
            x,y=token[1]; x1,y1,x2,y2=index
            #좌표 저장된 token[1]=(x,y)과 index비교
            if y1<=y<y2 and x1<=x<x2:
                if erase:
                    v.remove(token)
                    result=True
                else:
                    return True
    return result

icons = [] #UI를 위한 아이콘
# ——————————————고급설정 ——————————————
def open_advanced_form():
    #______________________함수 모음____________
    #content에 append도 자동 되도록 수정 이미 있다면 덮어쓰기
    def upload_img(category,img,folder_name): #예시: category default, folder_name sprites 
        data=load_content_json(project_dir)
        characterID=load_unique_id(data)
        if category=="default":
            filename = f"{characterID}.png"
        else:
            filename = f"{characterID}_{category}.png"
        save_path = os.path.join(project_dir, folder_name, filename)
        img.save(save_path)

        if folder_name=="sprites":
            targetF="Characters"
        elif folder_name=="portraits":
            targetF="Portraits"
        if category=="default":
            content={"Action": "Load","Target": f"{targetF}/{characterID}",
                    "FromFile": f"{folder_name}/{characterID}.png"
                    }
        elif category in ["summer","spring","fall","winter"]:
            categoryU=category.capitalize()
            content={
                "Action": "Load",
                "Target": f"{targetF}/{characterID}",
                "FromFile": f"{folder_name}/{characterID}_{category}.png",
	            "When": {
                    "Season": categoryU
                    }
                }
        else:
            content={
                "Action": "Load",
                "Target": f"{targetF}/{characterID}_{category}",
                "FromFile": f"{folder_name}/{characterID}_{category}.png"
            }
        mti=is_existing_data(content,data)
        append_to_content(content,data,mti)

        messagebox.showinfo("업로드 완료", f"{category} {folder_name}가 만들어졌습니다!")        
    def open_portrait_uploader():
        win = tk.Toplevel(root)
        win.title("초상화 불러오기")
        win.geometry("300x180")
        tk.Label(win, text="초상화 종류").pack(pady=10)
        season_combo = ttk.Combobox(win, values=["default", "spring", "summer", "fall", "winter","beach"], width=15)
        season_combo.pack()
        season_combo.set("default")

        # 업로드 핸들러 함수
        def upload():
            category = season_combo.get()
            file_path = filedialog.askopenfilename(title="초상화 선택", filetypes=[("PNG 이미지", "*.png"), ("모든 파일", "*.*")])
            if not file_path:
                return  # 사용자가 파일 선택 안 한 경우
            try:
                img = Image.open(file_path)
            except Exception as e:
                tk.messagebox.showerror("오류", f"이미지 열기 실패: {e}")
                return
            upload_img(category, img, "portraits")
            win.destroy()
        tk.Button(win, text="업로드", command=upload).pack(pady=20)
    def open_sprite_generator():
        win = tk.Toplevel(root)
        win.title("스프라이트 생성")
        win.geometry("500x600")

        data = load_content_json(project_dir)
        entries = data["Changes"]
        for change in entries:
            if change["Target"]=="Data/Characters":
                entries = change["Entries"]
                vals = list(entries.values())[0]
                break;
        gender=vals["Gender"]
        candance=vals.get("FlowerDanceCanDance")

        #xnb->png변환
        def unpack_xnb(xnb_path, out_dir):
            os.makedirs(out_dir, exist_ok=True)
            exe = os.path.join(os.getcwd(),"content","xnbcli","xnbcli.exe")
            try:
                subprocess.run([exe, "unpack", xnb_path, out_dir], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("오류",f"{xnb_path} 언팩 실패")
        # 모두 unpacked
        def allunpack(base_dir=r"C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley"):
            src=os.path.join(base_dir,"Content","Characters","Farmer")
            dst = os.path.join(os.getcwd(),"content","unpacked")
            if gender=="Female":
                base="farmer_girl_base"
            else:
                base="farmer_base"
            tup1=((18,21),(8,4*2),(8,14*3),(12,11*4),(12*10,21*2),(32,19*4),(4,19),(3,24))
            tup2=(1,2,3,4,12*21,4,4,3)
            Korean=("베이스","악세사리","머리", "모자","바지","옷","신발","피부")
            try:
                for i, xnb in enumerate((base, "accessories","hairstyles", "hats","pants","shirts","shoeColors","skinColors")):
                    xnb_path = os.path.join(src, f"{xnb}.xnb")
                    unpack_xnb(xnb_path, dst)
                    png=os.path.join(dst, f"{xnb}.png")
                    if os.path.isfile(png):
                        if (xnb=="hairstyles"):
                            xnb_path = os.path.join(src, "hairstyles2.xnb")
                            unpack_xnb(xnb_path, dst)
                            png=img_combined(Image.open(png), Image.open(os.path.join(dst, "hairstyles2.png")))
                            contents[xnb] = content(png, tup1[i][0], tup1[i][1],tup2[i],Korean[i])
                        elif xnb=="pants":
                            result=Image.new("RGBA", (1920, 1344), (0, 0, 0, 0))
                            result.paste(Image.open(png).crop((0,0,1920,672)),(0,0))
                            result.paste(Image.open(png).crop((0,688,1920,1360)),(0,672))
                            contents[xnb] = content(result, tup1[i][0], tup1[i][1], tup2[i], Korean[i])
                        else:
                            if i==0:
                                xnb="base"
                            contents[xnb] = content(Image.open(png), tup1[i][0], tup1[i][1], tup2[i], Korean[i])
            except:
                messagebox.showerror("오류","xnb를 불러오는 작업을 실패하였습니다. 정확한 게임 폴더를 선택해주세요")
                allunpack(filedialog.askdirectory(title="Stardew Valley 게임 폴더 선택"))
        #contents[파일명].data Image.image
        #contents[파일명].index(row,col) 사용가능(row행 col열 사진 반환)
        class content:
            def __init__(self, img, lenx, leny, num=1, name=None):
                self.data=img
                self.getx, self.gety=self.data.size
                self.lenx=lenx
                self.leny=leny #x,y방향으로 가진 토큰의 개수
                self.tokenx=self.getx//lenx
                self.tokeny=self.gety//leny #한 토큰의 크기(단위)
                self.num=num #한 선택지마다 가진 토큰의 개수
                self.sel=(lenx*leny)//num #선택지의 개수
                self.Korean=name #한글 이름
            def index (self, row, col):
                x1, y1=col*self.tokenx, row*self.tokeny
                x2, y2=x1+self.tokenx, y1+self.tokeny
                img=self.data.crop((x1,y1,x2,y2))
                return img
        def base_definition(colored=False, beach=False):
            if beach:
                beach=18
            tmp=contents["base"]
            resultbase=Image.new("RGBA", (64,128), (0, 0, 0, 0))
            resultarms=Image.new("RGBA", (64,128), (0, 0, 0, 0))
            for i in range(3) :
                for x, j in enumerate((0,2,0,1)):
                    resultbase.paste(tmp.index(i+beach,j),(x*16,i*32))
                    if beach:
                        resultarms.paste(tmp.index(19,5),(x*16,i*32))
                    else: resultarms.paste(tmp.index(i,j+6),(x*16,i*32))
                    if i==1:
                        resultbase.paste(ImageOps.mirror(tmp.index(i+beach,j)),(x*16,(i+2)*32))
                        if beach:
                            resultarms.paste(ImageOps.mirror(tmp.index(19,5)),(x*16,(i+2)*32))
                        else: resultarms.paste(ImageOps.mirror(tmp.index(i,j+6)),(x*16,(i+2)*32))
            results["base"]=content(resultbase,4,4)
            results["arms"]=content(resultarms,4,4)
            if colored:
                if shirts:
                    results["arms"].data=replace_color(results["arms"].data,(142,31,12,255),shirts[0].getpixel((0,2)),skincolors)
                    results["arms"].data=replace_color(results["arms"].data,(112,23,24,255),shirts[0].getpixel((0,3)),skincolors)
                    results["arms"].data=replace_color(results["arms"].data,(74,12,6,255),shirts[0].getpixel((0,4)),skincolors)
                if shoecolors:
                    results["base"].data=replace_color(results["base"].data,(85, 0, 0, 255),shoecolors[0])
                    results["base"].data=replace_color(results["base"].data,(91,31,36,255),shoecolors[1])
                    results["base"].data=replace_color(results["base"].data,(119,41,26,255),shoecolors[2])
                    results["base"].data=replace_color(results["base"].data,(173,71,27,255),shoecolors[3])
                if skincolors:
                    for i in range(3):
                        results["base"].data=replace_color(results["base"].data,basecolors[i],skincolors[i])
                        results["arms"].data=replace_color(results["arms"].data,basecolors[i],skincolors[i])
                results["base"].data=replace_color(results["base"].data,(104, 43, 15, 255),pickcolor[0]) 
        def multiply_color_preserve_transparency(base: Image.Image, color: tuple):
            base = base.convert("RGBA")
            try:
                r, g, b, _ = color
            except:
                r,g,b=color
            # 1. 곱할 색상으로 덮인 이미지 생성
            color_img = Image.new("RGBA", base.size, (r, g, b, 255))
            # 2. 곱하기 블렌딩
            blended_rgb = ImageChops.multiply(base.convert("RGB"), color_img.convert("RGB"))
            # 3. 원본 알파 채널 추출
            alpha = base.getchannel("A")
            # 4. 알파 채널 다시 붙이기 (투명도 보존)
            result = blended_rgb.convert("RGBA")
            result.putalpha(alpha)
            return result   
        def hair_colored():
            for i,hair in enumerate(hairs):
                hairs[i] = multiply_color_preserve_transparency(hair, pickcolor[1])
        def accs_colored(sel):
            if sel<=5 or (19<=sel and sel<=22):
                for i,acc in enumerate(accs):
                    accs[i] = multiply_color_preserve_transparency(acc, pickcolor[1])
        def pants_definition(selx,sely,beach=False):
            if beach:
                beach=18
            resultpants=Image.new("RGBA", (64,128), (0, 0, 0, 0))
            if gender=="Female":option=6
            else:option=0
            for i in range(3) : #ImageOps.mirror
                for x, j in enumerate((0,2,0,1)):
                    resultpants.paste(contents["pants"].index(sely+i+beach,selx+j+option),(16*x,32*i))
                    if i==1:
                        resultpants.paste(ImageOps.mirror(contents["pants"].index(sely+i+beach,selx+j+option)),(16*x,32*(i+2)))
            resultpants=multiply_color_preserve_transparency(resultpants, pickcolor[2])
            results["pants"]=content(resultpants,4,4)
        contents = {} #unpacked png 파일을 저장하는 변수
        allunpack()
        results={} #레이어별로 저장
        further_act={"base":[],"pants":[],"shirts":[],"accessories":[],"hairstyles":[],"hats":[],"arms":[]}#기본 스프라이트에서 유저가 추가하는 저장공간
        #리스트 안에 각각의 토큰 정보로 이루어진 리스트가 append되고, 0에 참조인덱스와 1에 붙여넣을 global좌표, 2에 반전여부가 저장된다 

        basecolors=[];skincolors=[];shoecolors=[];shirts=[];accs=[];hats=[];hairs=[];#토큰별 크롭 이미지 저장 변수
        pants=[]
        pickcolor=[(128, 64, 64),(128, 64, 64),(128, 64, 64)] #사용자 지정 색상 저장 변수
        for i in range(3):
            basecolors.append(contents["skinColors"].index(0, i).getpixel((0,0))) #recolored를 위한 순수색깔 저장
        base_definition()
        #GUI
        """
        애니메이션 사용자가 지정해서 조립하면 그걸 배열에 저장하고 사용자 선택 token 바뀔 때마다 재조립(배열대로 조립하는 함수(매개변수 key) 추가해서 on_select(key)각각에 넣음) 조립할 때는 다른 새옷, 새악세서리, 새바지,새머리 새모자 새베이스선택 새신발 불러오기도 가능해야함(추후 '새'것이 아닌 일반선택은 사용자의 선택에 따라 계속 바뀌어야함 특히 베이스의 모양은 조정되지 않지만 피부색이나 셔츠 (기존)신발은 색이 바뀌어야함)
        콤보박스 beach로 변경될 시 base, pants재정의 beach가 아닌 값으로 변경될 때도 재정의
        """
        class CharacterCreator:
                def __init__(self, parent):
                    self.selection = {k: v.sel - 1 for k, v in contents.items()}
                    self.frame = tk.Frame(parent)
                    self.frame.pack(fill="both", expand=True)
                    self.base_ref={} #추가 액션을 만들 때 사용하는 변수(참조 베이스 인덱스 저장 변수)
                    #한글 레이어의 순서는 팔보다 셔츠가 위로 올라가면 안됨(new shirts 색깔을 저장한 후 arms에서 참조해야 하므로)
                    self.layers_Korean=["피부", "바지", "셔츠", "악세서리", "헤어", "모자", "팔"] #레이어 정렬을 위해 필요한 리스트, 헤어 팔 순서 조정 가능
                    self.layers_English=["base","pants","shirts","accessories","hairstyles","hats","arms"]
                    # 상단 계절 콤보박스
                    top_frame = tk.Frame(self.frame)
                    top_frame.pack(side="top", pady=5)
                    tk.Label(top_frame, text="스프라이트 종류").pack(side="left")
                    self.season_combo = ttk.Combobox(top_frame, values=["default", "spring", "summer", "fall", "winter","beach"], width=10)
                    self.season_combo.pack(side="left")
                    self.season_combo.set("default")
                    
                    self.isbeach=False
                    # beach 선택 시 isbeach = True, 아니면 False
                    def on_season_change(event=None):
                        selected = self.season_combo.get()
                        self.isbeach = (selected == "beach")
                        for k,v in contents.items():
                            if k!="base":
                                self.result_ctrl(k)
                        self.redraw()
                    self.season_combo.bind("<<ComboboxSelected>>", on_season_change)


                    # 왼쪽 컨트롤 패널
                    ctrl = tk.Frame(self.frame)
                    ctrl.pack(side="left", fill="y", padx=5, pady=5)

                    for k,v in contents.items():
                        if k!="base":
                            tk.Label(ctrl, text=v.Korean, width=12).pack(anchor="w")
                            combo = ttk.Combobox(ctrl, values=list(range(v.sel)), width=10, state="readonly")
                            combo.current(0)
                            combo.pack(pady=2)
                            combo.bind("<<ComboboxSelected>>", #콤보박스의 값이 바뀌었다면
                                   lambda ev, ln=k, cb=combo: self.on_select(ln, int(cb.get())))
                            self.result_ctrl(k)
                    tk.Button(ctrl, text="내보내기", command=self.export_png).pack(pady=10)
        
                    # 오른쪽 옵션
                    right = tk.Frame(self.frame)
                    right.pack(side="right", fill="y", padx=10)
                    self.color_buttons = {}
                    for color_name in ["눈 색", "머리 색", "바지 색"]:
                        frame = tk.Frame(right)
                        frame.pack(pady=5)
                        tk.Label(frame, text=color_name).pack()
                        btn = tk.Button(frame, text="선택", command=lambda cn=color_name: self.pick_color(cn))
                        btn.pack()
                        self.color_buttons[color_name] = btn
                    tk.Button(right, text="액션 추가", command=self.further_act_ctrl).pack(pady=10)
                    
                    # 하단 문구
                    tk.Label(self.frame, text="※ 큰 모자 등 잘리는 이미지는 게임에서도 진짜 잘립니다", fg="red").pack(side="bottom", pady=3)
                    tk.Label(self.frame, text="※ 게임 파일 내에 리텍된 xnb를 넣어 합칠 수 있습니다.\nnpc를 배포할 계획이 있다면\n꼭 해당 파일의 사용범위를 검토해주세요", justify="center").pack(side="bottom")

                    # 미리보기 캔버스
                    self.canvas_size=(800//results["base"].leny,400)
                    self.canvas = tk.Canvas(self.frame, width=self.canvas_size[0], height=self.canvas_size[1])
                    self.canvas.pack(padx=10, pady=10,expand=True,anchor="center")
                    self.canvas_channel=0

                    self.RotateIconF=tk.Frame(self.frame)
                    self.RotateIconF.pack(side="bottom", pady=10)
                    # 아이콘 이미지 불러오기 및 크기 조정
                    left_icon_raw = Image.open(os.path.join(os.getcwd(), "content", "icon", "왼쪽화살표.png"))
                    left_icon_resized = left_icon_raw.resize((left_icon_raw.width // 2, left_icon_raw.height // 2), Image.LANCZOS)
                    self.left_icon_img = ImageTk.PhotoImage(left_icon_resized)

                    right_icon_raw = ImageOps.mirror(left_icon_raw)
                    right_icon_resized = right_icon_raw.resize((right_icon_raw.width // 2, right_icon_raw.height // 2), Image.LANCZOS)
                    self.right_icon_img = ImageTk.PhotoImage(right_icon_resized)

                    # 테두리 없는 세련된 버튼 생성
                    self.left_btn = tk.Button(self.RotateIconF,
                          image=self.left_icon_img,
                          command=self.leftsignal,
                          relief="flat",
                          borderwidth=0)
                    self.left_btn.pack(side="left", padx=10)  # 간격 조정

                    self.right_btn = tk.Button(self.RotateIconF,
                           image=self.right_icon_img,
                           command=self.rightsignal,
                           relief="flat",
                           borderwidth=0)
                    self.right_btn.pack(side="left", padx=10)  # 간격 조정

                    self.redraw()             
                def pick_color(self, label): #라벨 ["눈 색", "머리 색", "바지 색"] 중
                    color = colorchooser.askcolor(title=f"{label} 선택")[0]
                    if color:
                        if label=="눈 색":
                            pickcolor[0]=color
                            base_definition(True, self.isbeach)
                            self.further_act_definition("base")
                            self.redraw()
                        if label=="머리 색":
                            pickcolor[1]=color
                            self.result_ctrl("hairstyles")
                            self.result_ctrl("accessories")
                            self.redraw()
                        if label=="바지 색":
                            pickcolor[2]=color
                            self.result_ctrl("pants")
                            self.redraw()
                def on_select(self, key, user_sel): #선택바뀔 때
                    self.selection[key] = user_sel
                    self.result_ctrl(key)
                    self.redraw()
                def leftsignal(self):
                    self.canvas_channel=(results["base"].leny+self.canvas_channel)%(results["base"].leny+1)
                    self.redraw()
                def rightsignal(self):
                    self.canvas_channel=(self.canvas_channel+1)%(results["base"].leny+1)
                    self.redraw()
                def result_ctrl(self,key): #입력된 키에 따라 rsult에 토큰 재배치
                    sel=self.selection[key]
                    basetmp=results["base"]
                    if key!="pants":
                        results[key]=content(Image.new("RGBA", basetmp.data.size, (0, 0, 0, 0)) ,basetmp.lenx, basetmp.leny)
                    tmp=contents[key]
                    if key=="hats":
                        hats.clear()
                        for i in range(4):
                            hats.append(tmp.index((sel//tmp.lenx)*4+i, sel%tmp.lenx))
                        wid,hei=hats[0].size
                        if gender=="Female":option=1
                        else:option=0
                        if self.isbeach: beach=2
                        else:beach=0
                        hats_moving=((2,1,2,1),
                                     (3,2,3,2),
                                     (2,1,2,1),
                                     (3,2,3,2))
                        for i, x in enumerate((0,1,3,2)):
                            for j in range(basetmp.lenx):
                                results[key].data.paste(hats[x].crop((2,beach+hats_moving[i][j]-option,wid-2,hei)),
                                                        (basetmp.tokenx*j,basetmp.tokeny*i))
                        self.further_act_definition(key)
                    elif key=="accessories": 
                        accs.clear()

                        for i in range(2):
                            accs.append(tmp.index((sel//tmp.lenx)*2+i, sel%tmp.lenx))
                        accs_colored(sel)
                        if gender=="Female":option=1
                        else:option=0
                        if self.isbeach:beach=2
                        else: beach=0
                        accs_moving=((2,3,2,3),
                                     (2,3,2,3))
                        for i in range(2):
                            for j in range(basetmp.lenx):
                                results[key].data.paste(accs[i],(basetmp.tokenx*j,
                                                                 basetmp.tokeny*i+accs_moving[i][j]+option-beach))
                        for i in range(4):
                            results[key].data.paste(ImageOps.mirror(results[key].index(1,i)),
                                                                    (basetmp.tokenx*i,basetmp.tokeny*3))
                        self.further_act_definition(key)
                    elif key=="hairstyles":
                        hairs.clear()
                        option=0;option2=0;option3=0;
                        if sel>=56:
                            option=1 #헤어스타일2
                        elif sel>=16:
                            option2=1
                        if gender=="Female":
                            option3=1
                        if self.isbeach:beach=2
                        else: beach=0
                        for i in range(3+option):
                            if option:
                                hairs.append(tmp.index(21+((sel-56)//tmp.lenx)*4+i, sel%tmp.lenx))
                            else:
                                hairs.append(tmp.index((sel//tmp.lenx)*3+i, sel%tmp.lenx))
                        hair_colored()

                        hairs_moving=((1,2,1,2),
                                     (1,2,1,2),
                                     (1,2,1,2))
                        for i in range(3):
                            for j in range(basetmp.lenx):
                                results[key].data.paste(hairs[i],(basetmp.tokenx*j,
                                                                 basetmp.tokeny*i+hairs_moving[i][j]-option-option2+option3-beach))
                        for i in range(4):
                            if option:
                                results[key].data.paste(hairs[3],(basetmp.tokenx*i,
                                                                  basetmp.tokeny*3+hairs_moving[1][i]-option+option3-beach))
                            else:
                                results[key].data.paste(ImageOps.mirror(results[key].index(1,i)),
                                                                    (basetmp.tokenx*i,basetmp.tokeny*3))
                        self.further_act_definition(key)
                    elif key=="pants":
                        pants.clear()
                        selx=12*(sel%10)
                        sely=21*(sel//10)
                        pants.append(selx);pants.append(sely)
                        pants_definition(selx,sely,self.isbeach)
                        self.further_act_definition("pants")
                    elif key=="shirts":
                        shirts.clear()
                        for i in range(4):
                            shirts.append(tmp.index((sel//tmp.lenx)*4+i, sel%tmp.lenx))
                        if gender=="Female":option=1
                        else:option=0
                        if self.isbeach:beach=2
                        else: beach=0
                        for x, i in enumerate((0,1,3,2)):
                            addx=4;addy=15
                            if x==2:
                                addy-=1
                                if beach:
                                    beach=1
                            else:
                                if beach:
                                    beach=2
                            for j in range(basetmp.lenx):
                                results[key].data.paste(shirts[i],(basetmp.tokenx*j+addx,
                                                                 basetmp.tokeny*x+addy+j%2+option-beach))
                        self.further_act_definition(key)
                        base_definition(True,self.isbeach)
                        self.further_act_definition("base")
                    elif key=="shoeColors":
                        shoecolors.clear()
                        for i in range(4):
                            shoecolors.append(tmp.index(sel, i).getpixel((0,0)))
                        base_definition(True,self.isbeach)
                        self.further_act_definition("base")
                    elif key=="skinColors":
                        skincolors.clear()
                        for i in range(3):
                            skincolors.append(tmp.index(sel, i).getpixel((0,0)))
                        base_definition(True,self.isbeach)
                        self.further_act_definition("base")
                def further_act_definition(self,key): #입력된 키에 따라 further_act에 저장된 값을 보고 토큰 재배치
                    #외부에서 lenx leny 항상 갱신하고 이 함수로 들어옴
                    #further_act={key: [참조인덱스 row col ,[x,y],반전여부],[],...}
                    token=further_act[key]
                    if token and (key=="base"):
                            resultbase=Image.new("RGBA", (64,results["pants"].leny*32), (0, 0, 0, 0)) #base_definition으로 인해 4*4로 된 상태이므로 pants참조
                            resultarms=Image.new("RGBA", (64,results["pants"].leny*32), (0, 0, 0, 0))
                    elif token and (key=="pants"):
                            resultpants=Image.new("RGBA", (64,results["base"].leny*32), (0, 0, 0, 0))
                    for i,tmp in enumerate(token):
                        if key=="base":
                            tokena=further_act["arms"]
                            tokenarms=contents["base"].index(tokena[i][0][0],tokena[i][0][1])
                            if not tokena[i][3]:#새로운 셔츠가 아닐 때만 옷 부분 기존 색으로 컬러링
                                if shirts:
                                    tokenarms=replace_color(tokenarms,(142,31,12,255),shirts[0].getpixel((0,2)),skincolors)
                                    tokenarms=replace_color(tokenarms,(112,23,24,255),shirts[0].getpixel((0,3)),skincolors)
                                    tokenarms=replace_color(tokenarms,(74,12,6,255),shirts[0].getpixel((0,4)),skincolors)
                            else: #새로운 셔츠(독립변수)면 기존 색 다시 입혀줌
                                tokenarms=replace_color(tokenarms,(142,31,12,255),tokena[i][3][0],skincolors)
                                tokenarms=replace_color(tokenarms,(112,23,24,255),tokena[i][3][1],skincolors)
                                tokenarms=replace_color(tokenarms,(74,12,6,255),tokena[i][3][2],skincolors)
                            if tmp[2]: #반전여부 True면
                                resultbase.paste(ImageOps.mirror(contents["base"].index(tmp[0][0],tmp[0][1])),tuple(tmp[1]))
                                resultarms.paste(ImageOps.mirror(tokenarms),tuple(tokena[i][1]))
                            else: #반전 아니면
                                resultbase.paste(contents["base"].index(tmp[0][0],tmp[0][1]),tuple(tmp[1]))
                                resultarms.paste(tokenarms ,tuple(tokena[i][1]))
                        elif key=="pants":
                            if tmp[2]:
                                resultpants.paste(ImageOps.mirror(contents["pants"].index(pants[1]+tmp[0][0],pants[0]+tmp[0][1])),tuple(tmp[1]))
                            else:
                                resultpants.paste(contents["pants"].index(pants[1]+tmp[0][0],pants[0]+tmp[0][1]),tuple(tmp[1]))
                        elif key=="hats":
                            if tmp[2]:
                                results[key].data.paste(ImageOps.mirror(hats[tmp[0]]),tuple(tmp[1]))
                            else:
                                results[key].data.paste(hats[tmp[0]],tuple(tmp[1]))
                        elif key=="accessories":
                            if tmp[2]:
                                results[key].data.paste(ImageOps.mirror(accs[tmp[0]]),tuple(tmp[1]))
                            else:
                                results[key].data.paste(accs[tmp[0]],tuple(tmp[1]))
                        elif key=="hairstyles":
                            if tmp[2]:
                                results[key].data.paste(ImageOps.mirror(hairs[tmp[0]]),tuple(tmp[1]))
                            else:
                                results[key].data.paste(hairs[tmp[0]],tuple(tmp[1]))
                        elif key=="shirts":
                            if tmp[2]:
                                results[key].data.paste(ImageOps.mirror(shirts[tmp[0]]),tuple(tmp[1]))
                            else:
                                results[key].data.paste(shirts[tmp[0]],tuple(tmp[1]))
                    if token and (key=="base"):
                            if shoecolors:
                                resultbase=replace_color(resultbase,(85, 0, 0, 255),shoecolors[0])
                                resultbase=replace_color(resultbase,(91,31,36,255),shoecolors[1])
                                resultbase=replace_color(resultbase,(119,41,26,255),shoecolors[2])
                                resultbase=replace_color(resultbase,(173,71,27,255),shoecolors[3])
                            if skincolors:
                                for i in range(3):
                                    resultbase=replace_color(resultbase,basecolors[i],skincolors[i])
                                    resultarms=replace_color(resultarms,basecolors[i],skincolors[i])
                            resultbase=replace_color(resultbase,(104, 43, 15, 255),pickcolor[0])
                            resultbase.paste(results["base"].data,(0,0))
                            resultarms.paste(results["arms"].data,(0,0))
                            results["base"]=content(resultbase,4,results["pants"].leny)
                            results["arms"]=content(resultarms,4,results["pants"].leny)
                    elif token and (key=="pants"):
                            resultpants=multiply_color_preserve_transparency(resultpants, pickcolor[2])
                            resultpants.paste(results[key].data,(0,0))
                            results[key]=content(resultpants,4,results["base"].leny) 
                #스프라이트의 추가적인 액션 관리자
                def further_act_ctrl(self, further_act_name=None, further_act_index=None):
                    characterID=load_unique_id(data)
                    #txt 경로, 없다면 생성
                    txt_path = os.path.join(os.getcwd(), "content", "user_data", "animation_data", f"{characterID}.txt")
                    if not os.path.isfile(txt_path):
                            frame_count = results["base"].leny * 4  # 예: 기본 프레임 수 * 4
                            newdata = []
                            if frame_count>16:
                                for i in range(frame_count)[16:]:
                                    newdata.append(f"{i}//\n")
                            with open(txt_path, "w", encoding="utf-8") as f:
                                f.writelines(newdata)
                    with open(txt_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    #추가할 애니메이션데이터 불러오기
                    new_anims = load_animation_data(lines)
                    if further_act_name:
                        if further_act_index:
                            try: #액션명이 이미 정의되어 있다면
                                if not further_act_index in new_anims[further_act_name]:
                                    new_anims[further_act_name].append(further_act_index)
                            except:
                                new_anims[further_act_name]=[]
                                new_anims[further_act_name].append(further_act_index)
                    if isromance():
                            if vals.get("KissSpriteIndex"):
                                new_anims["키스"] = [vals["KissSpriteIndex"]]
                            else:
                                new_anims["키스"] = [28]
                            if candance!=False:
                                if gender=="Female":
                                    new_anims["결혼"] = [36, 37, 38]
                                    new_anims["플라워댄스"] = [40, 41, 42, 43, 44, 45, 46, 47]
                                else:
                                    new_anims["플라워댄스"] = [44, 45, 46, 47]
                                    new_anims["결혼"] = [48, 49, 50, 51]
                    elif candance:
                        if gender=="Female":
                            new_anims["플라워댄스"] = [40, 41, 42, 43, 44, 45, 46, 47]
                        else:
                            new_anims["플라워댄스"] = [44, 45, 46, 47]

                    #GUI
                    win2 = tk.Toplevel(win)
                    win2.title("스프라이트 추가")
                    frame_height = min(max(len(new_anims) * 170, 150), 600)
                    win2.geometry(f"300x{frame_height}")
                    scroll_frame = tk.Frame(win2)
                    scroll_frame.pack(fill="both", expand=True)

                    canvas = tk.Canvas(scroll_frame)
                    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
                    canvas.configure(yscrollcommand=scrollbar.set)

                    scrollbar.pack(side="right", fill="y")
                    canvas.pack(side="left", fill="both", expand=True)

                    # 스크롤 가능한 내부 프레임
                    scrollable_frame = tk.Frame(canvas)
                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    # 내부 프레임 사이즈가 바뀌면 캔버스 스크롤 영역 재조정
                    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


                    #리스트박스 업데이트
                    def display_on_listbox(new_anims,scrollable_frame,action_entry,frame_entry,on_add):
                        for key in list(new_anims.keys()):
                            if not new_anims[key]:
                                del new_anims[key]
                        for widget in scrollable_frame.winfo_children():
                                if isinstance(widget,tk.Listbox):
                                    widget.destroy()
                                if isinstance(widget,tk.Label) and not (widget.cget("text").startswith("스프라이트의 몇 번째 인덱스에 어떤 액션을")):
                                    widget.destroy()
                                    
                        if not new_anims:
                            tk.Label(scrollable_frame, text="데이터 없음").pack()
                            return
                        # 각 애니메이션 이름별로 Listbox 표시
                        for name, frame_list in new_anims.items():
                            tk.Label(scrollable_frame, text=name, font=("맑은 고딕", 10, "bold")).pack(anchor="w", pady=(10, 0))
                            # 리스트 박스 높이: frame_list 길이만큼 (최소 2, 최대 10)
                            listbox_height = min(max(len(frame_list), 2), 10)
                            listbox = tk.Listbox(scrollable_frame, height=listbox_height)
                            for frame in frame_list:
                                listbox.insert(tk.END, frame)
                            # 리스트박스 더블클릭 이벤트
                            def on_double_click(event, act_name=name, listbox_ref=listbox): #더블클릭 추가
                                try:
                                    on_cb_click(event, act_name, listbox_ref)
                                    on_add()
                                except:
                                    return
                            def on_cb_click(event, act_name=name, listbox_ref=listbox): #클릭하면 텍스트박스값 바뀜
                                try:
                                    action_entry.delete(0,tk.END)
                                    action_entry.insert(0,act_name)
                                    frame_entry.delete(0,tk.END)
                                    frame_entry.insert(0,listbox_ref.get(listbox_ref.curselection()))
                                except:
                                    return
                            listbox.bind("<Double-Button-1>", on_double_click)
                            listbox.bind("<<ListboxSelect>>", on_cb_click)
                            listbox.pack(padx=5, pady=3, fill="x")
                    tk.Label(scrollable_frame, text="스프라이트의 몇 번째 인덱스에 어떤 액션을\n넣을지 입력하세요. 액션명이 같은 스프라이트는\n추후에 동일한 카테고리로 취급됩니다\n또는 박스의 항목 더블클릭").pack(side="top")
                    
                    # 추가용 입력 필드
                    entry_frame = tk.Frame(scrollable_frame)
                    entry_frame.pack(side="top",pady=10)

                    tk.Label(entry_frame, text="액션이름").grid(row=0, column=0)
                    action_entry = tk.Entry(entry_frame,width=10)
                    action_entry.grid(row=0, column=1)
                    tk.Label(entry_frame, text="인덱스").grid(row=0, column=2)
                    frame_entry = tk.Entry(entry_frame,width=5)
                    frame_entry.grid(row=0, column=3)
                    #추가 버튼
                    def on_add():
                        act_name = action_entry.get().strip()
                        try:
                            act_index = int(frame_entry.get())
                            if act_index<16:
                                messagebox.showerror("오류", "걷는 모션이 있는 자리입니다")
                                return
                        except ValueError:
                            messagebox.showerror("오류", "프레임 인덱스는 숫자여야 합니다")
                            return
                        if act_name:
                            for k,v in new_anims.items():
                                for index in v:
                                    if act_index==index:
                                        if k==act_name:
                                            if isinsprite(further_act, int(index)):
                                                response=messagebox.askyesno("확인","해당하는 인덱스에 데이터가 이미 존재합니다. 지우고 다시 시작합니까?")
                                                if response:
                                                    self.further_act_del(index)
                                                else:
                                                    return
                                        else: #인덱스는 같은데 액션명이 다르면
                                            response=messagebox.askyesno("새로운 이름",f"해당하는 인덱스의 액션 데이터를 업데이트합니까? 확인을 누르면 {index}번째의 {k}액션 자체가 사라집니다. 액션 데이터는 모든 스프라이트가 공유합니다")
                                            if response:
                                                if isinsprite(further_act, int(index)):
                                                    self.further_act_del(index)
                                                new_anims[k].remove(act_index)
                                                update_lines(new_anims,txt_path)
                                            else: return
                            self.further_act_edit(act_name, act_index)
                            win2.destroy()

                        else:
                            messagebox.showerror("오류", "공백은 불가능합니다")
                            return
                    display_on_listbox(new_anims,scrollable_frame,action_entry,frame_entry,on_add)
                    #삭제 버튼
                    def on_delete():
                        found=False
                        try:
                            act_index = int(frame_entry.get())
                            if act_index<16:
                                messagebox.showerror("오류", "걷는 모션이 있는 자리입니다")
                                return
                        except ValueError:
                            messagebox.showerror("오류", "프레임 인덱스는 숫자여야 합니다")
                            return
                        for k in list(new_anims.keys()):
                            v=new_anims[k]
                            for index in v:
                                if act_index==index:
                                    response=messagebox.askyesno("확인","모든 스프라이트들이 공유하는 데이터입니다. 해당 스프라이트에서만 데이터를 없애려면 '지우기'기능을 사용하세요. 정말 액션을 삭제하시겠습니까?")
                                    if response:
                                        if isinsprite(further_act, int(index)):
                                            self.further_act_del(index)
                                        new_anims[k].remove(act_index)
                                        update_lines(new_anims,txt_path)
                                        display_on_listbox(new_anims,scrollable_frame,action_entry,frame_entry,on_add)
                                    found=True
                        if not found:
                            messagebox.showerror("오류", "해당하는 인덱스가 존재하지 않습니다")
                            return
                    #지우기 버튼
                    def on_clear():
                        try:
                            act_index = int(frame_entry.get())
                            if act_index<16:
                                messagebox.showerror("오류", "걷는 모션이 있는 자리입니다")
                                return
                        except ValueError:
                            messagebox.showerror("오류", "프레임 인덱스는 숫자여야 합니다")
                            return
                        if isinsprite(further_act,act_index):
                            messagebox.showinfo("안내",f"{act_index}번째 스프라이트를 지웠습니다. 액션데이터는 사라지지 않습니다")
                            self.further_act_del(act_index)
                        else:
                            messagebox.showerror("오류", "해당 인덱스에 데이터가 존재하지 않습니다")
                            return
                    tk.Button(entry_frame, text="추가", command=on_add).grid(row=1, column=0,pady=5)
                    tk.Button(entry_frame, text="삭제", command=on_delete).grid(row=1, column=1,pady=5)
                    tk.Button(entry_frame, text="지우기", command=on_clear).grid(row=1, column=2,pady=5)
                    
                    def update_lines(new_anims, txt_path):#lines data 업데이트
                        new_lines=""
                        for anim_name, indices in new_anims.items():
                            indices=sorted(indices)
                            for idx_offset, frame_idx in enumerate(indices):
                                new_lines+=f"{frame_idx}/{anim_name}/{idx_offset}\n"
                        #다시 파일로 저장
                        with open(txt_path, "w", encoding="utf-8") as f:
                            f.writelines(new_lines) #애니메이션 관리자
                    update_lines(new_anims, txt_path)
                def further_act_del(self,index): #애니메이션 자체를 삭제하진 않고 results와 further_act를 관리함
                    #index=(row,col)
                    row=index//4
                    col=index%4
                    if isinsprite(further_act,(row,col)): #토큰이 존재하는데 further_act에 데이터가 없을수는 없음 base때문에라도
                        for k,v in results.items():
                            v.data=erase_region(v.data, (row,col))
                        isinsprite(further_act, (row,col), erase=True) #입력받은 index에 해당하는 이미지 지움
                    else:
                        messagebox.showerror("오류","해당 인덱스에 데이터가 존재하지 않습니다")
                        return #없다면 사용자에게 알림
                    basetmp=results["base"]
                    maxrow=3
                    for r in range(basetmp.leny-1,-1,-1): #0~leny-1 역순
                        for c in range(3,-1,-1): #0~3 역순
                            if isinsprite(further_act, (r,c)):
                                maxrow=r
                    if maxrow<basetmp.leny-1: #만약에 갱신된 maxrow가 기존 leny보다 작으면
                        for key in results:
                            results[key]=content(results[key].data.crop((0,0,4*16,(maxrow+1)*32)),4,maxrow+1)
                    self.redraw()
                def further_act_edit(self, act_name, act_index):
                    win2 = tk.Toplevel(win)
                    win2.title(f"{act_index}번 {act_name} 정의")
                    win2.geometry("500x450")

                    self.last_selected_part = None
                    # 왼쪽 컨트롤 패널
                    ctrl = tk.Frame(win2)
                    ctrl.pack(side="left", fill="y", padx=5, pady=5)
                    ctrl_key={"피부":"base", "바지":"pants","팔":"base","셔츠":"shirts",
                              "악세서리":"accessories","헤어":"hairstyles","모자":"hats"}
                    ctrl_index={"피부":(6,21), "바지":(6,21),"팔":(12,21),"셔츠":["앞","R","L","뒤","없음"],
                              "악세서리":["앞","R","L","없음"],"헤어":["앞","R","뒤","L","없음"],"모자":["앞","R","L","뒤","없음"]}
                    self.ctrl_key=ctrl_key
                    self.ctrl_index=ctrl_index
                    #특정항목에 L이 존재하지 않을 수도 있는데 그러면(except) R 반전시키고 반전여부 True
                    #셔츠 악세서리 헤어 모자 등등은 hats[0](앞을 뜻함) 등으로 전역변수에 img로 저장되어있음
                    #"팔"의 경우 further_act 에 key=arms로 저장됨

                    self.isfix=True
                    self.basemirrored=False
                    #팔 피부 바지 고정 기능
                    def fix_handler():
                        if self.isfix:
                            self.isfix=False
                            self.fix_btn.config(text="고정")
                        else:
                            self.isfix=True
                            self.fix_btn.config(text="고정해제")
                    self.selections = {}
                    #key: [옵션cb, 참조인덱스cb, 좌표, 반전여부 False]
                    
                    # 왼쪽 UI
                    left_frame = tk.Frame(win2)
                    left_frame.pack(side="left", fill="y", padx=5, pady=5)
                    ctrl = tk.Frame(left_frame)
                    ctrl.pack(side="top",fill="x",pady=5)
                    
                    row=0
                    for part, key in ctrl_key.items():
                        col=0
                        tk.Label(ctrl, text=part).grid(row=row,column=col)
                        col+=1
                        self.selections[part]=[]
                        if isinstance(ctrl_index[part], tuple): #피부, 바지, 팔
                            if part=="바지":
                                option_cb=ttk.Combobox(ctrl, values=["기본"]+list(range(contents[key].sel)), width=4,state="readonly")
                                option_cb.current(0)
                                option_cb.grid(row=row,column=col)
                                col+=1
                                self.selections[part].append(option_cb)
                            else: self.selections[part].append(None)
                            dir_cb = ttk.Combobox(ctrl, values=list(range(ctrl_index[part][0]*ctrl_index[part][1])), width=4,state="readonly")
                            dir_cb.current(0)
                        else:
                            option_cb=ttk.Combobox(ctrl, values=["기본"]+list(range(contents[key].sel)), width=4,state="readonly")
                            option_cb.current(0)
                            option_cb.grid(row=row,column=col)
                            col+=1
                            self.selections[part].append(option_cb)
                            # 그 외는 방향 선택
                            dir_cb = ttk.Combobox(ctrl, values=ctrl_index[part], width=6,state="readonly")
                            dir_cb.current(len(ctrl_index[part])-1)
                        dir_cb.grid(row=row,column=col)
                        row+=1

                        self.selections[part].append(dir_cb)
                        self.selections[part].append([0,0])
                        self.selections[part].append(self.basemirrored)
                        #[기본/0~contents[v].sel까지 택1] 라벨k [피부/바지/팔이라면 콤보박스 두개만들어서 (0~6)(0~21) 중에 고르고 다른 거라면
                    self.fix_btn = tk.Button(ctrl, text="고정해제", command=fix_handler)
                    self.fix_btn.grid(row=0,column=2)
                    tk.Label(ctrl, text="━━┘").grid(row=2,column=2)
                    tk.Label(left_frame,text="👆개체 선택 후 방향키로 위치 조절 가능\n📌기본 옵션 선택 시 다른 인덱스들의\n개체와 함께 변경됩니다. 기본이 아닐 경우\n독립적인 개체가 되어 변경되지 않습니다").pack()

                    if act_name=="키스":
                            if vals.get("KissSpriteFacingRight")==False:
                                self.basemirrored=True
                            else:
                                self.basemirrored=False
                            self.selections["피부"][1].current(101)
                            self.selections["바지"][1].current(101)
                            self.selections["팔"][1].current(197)
                    else:
                            if isromance() or candance==True:
                                if gender=="Female":
                                    #여자결혼
                                    if act_index==37: 
                                            self.selections["피부"][1].current(6)
                                            self.selections["바지"][1].current(6)
                                            self.selections["팔"][1].current(12)
                                    elif act_index==38:
                                            self.selections["피부"][1].current(101)
                                            self.selections["바지"][1].current(101)
                                            self.selections["팔"][1].current(197)
                                    #여자플댄
                                    elif act_index==41:
                                            self.selections["피부"][1].current(66)
                                            self.selections["바지"][1].current(66)
                                            self.selections["팔"][1].current(29)
                                            fix_handler()
                                    elif act_index==42:
                                            self.selections["피부"][1].current(66)
                                            self.selections["바지"][1].current(66)
                                            self.selections["팔"][1].current(29)
                                            fix_handler()
                                            self.basemirrored=True
                                    elif act_index==43:
                                            self.selections["피부"][1].current(70)
                                            self.selections["바지"][1].current(70)
                                            self.selections["팔"][1].current(24)
                                            self.selections["팔"][2][1]+=1
                                            fix_handler()
                                    elif act_index==44:
                                            self.selections["피부"][1].current(1)
                                            self.selections["바지"][1].current(1)
                                            self.selections["팔"][1].current(2)
                                            fix_handler()
                                    elif act_index==45:
                                            self.selections["피부"][1].current(2)
                                            self.selections["바지"][1].current(2)
                                            self.selections["팔"][1].current(1)
                                            fix_handler()
                                    elif act_index==46:
                                            self.selections["피부"][1].current(0)
                                            self.selections["바지"][1].current(0)
                                            self.selections["팔"][1].current(30)
                                            self.selections["팔"][2][1]+=1
                                            fix_handler()
                                    elif act_index==47:
                                            self.selections["피부"][1].current(67)
                                            self.selections["바지"][1].current(67)
                                            self.selections["팔"][1].current(31)
                                            self.selections["팔"][2][1]+=1
                                            fix_handler()
                                else:
                                    #남자결혼
                                    if act_index==49:
                                            self.selections["피부"][1].current(6)
                                            self.selections["바지"][1].current(6)
                                            self.selections["팔"][1].current(12)
                                    elif act_index==50:
                                            self.selections["피부"][1].current(101)
                                            self.selections["바지"][1].current(101)
                                            self.selections["팔"][1].current(197)
                                    #남자 플댄
                                    elif act_index==44:
                                            self.selections["피부"][1].current(12)
                                            self.selections["바지"][1].current(12)
                                            self.selections["팔"][1].current(24)
                                    elif act_index==45:
                                            self.selections["피부"][1].current(63)
                                            self.selections["바지"][1].current(63)
                                            self.selections["팔"][1].current(0)
                                            self.selections["팔"][2][1]+=1
                                            fix_handler()
                                    elif act_index==46:
                                            self.selections["피부"][1].current(13)
                                            self.selections["바지"][1].current(13)
                                            self.selections["팔"][1].current(26)
                                            fix_handler()
                                    elif act_index==47:
                                            self.selections["피부"][1].current(14)
                                            self.selections["바지"][1].current(14)
                                            self.selections["팔"][1].current(25)
                                            fix_handler()  #넘겨받은 act명에 따라 초기선택 배치

                    # 미리보기 캔버스
                    self.act_canvas_size=(200,400)
                    self.act_canvas = tk.Canvas(win2, width=self.act_canvas_size[0], height=self.act_canvas_size[1])
                    self.act_canvas.pack(padx=10, pady=10)

                    self.new_shirt=[] #새로운 셔츠를 정의할 경우 이 곳에서 색을 참조
                    #self.further_act_ctrl(act_name, act_index) 호출하고 데이터 leny 크기 늘리고 results 각각의 레이어에다가 갖다붙 이고 창 닫기
                        #기본이 아닌 독립변수들은 hats23 과 같은 형태의 키로 results에 붙이고 기본인건
                        #further_act 전역변수와 result에 붙이고
                        #후에  redraw에서 이러한 유사키레이어 들도 모두 정렬해야함
                    def save_and_close():
                        isnewshirts=None
                        for part in self.layers_Korean:
                            default=True
                            normal=False
                            sel=self.selections[part]
                            if sel[1].get()!="없음":
                                if sel[0]:
                                    if sel[0].get()!="기본": #기본이 아니면 독립변수로 저장안함
                                        default=False
                                        if part=="셔츠":
                                            isnewshirts=self.new_shirt
                                if default:
                                    if part=="팔": current_key="arms"
                                    else: current_key=ctrl_key[part]
                                    if part=="팔" or part=="피부" or part=="바지":
                                        ref=self.base_ref[part]
                                    else:
                                        normal=True
                                        ref=int(ctrl_index[part].index(sel[1].get()))
                                    basetmp=results["base"]
                                    x_global=(act_index%basetmp.lenx)*basetmp.tokenx+sel[2][0]
                                    y_global=(act_index//basetmp.lenx)*basetmp.tokeny+sel[2][1]
                                    # 참조 contents 인덱스, 붙여넣기 좌표list, 반전여부, 새로운 셔츠인지(팔 컬러링할지 구분하기 위해)
                                    if sel[3] and normal: #L가 존재하지 않는 일반 토큰&반전여부
                                        further_act[current_key].append([1,[x_global,y_global],sel[3],isnewshirts])
                                    else:
                                        further_act[current_key].append([ref,[x_global,y_global],sel[3],isnewshirts])
                        for k,v in results.items(): #작다면 확장
                            newy=act_index//4+1
                            if newy>v.leny:
                                tmpdata=Image.new("RGBA", (4*16, newy*32), (0, 0, 0, 0))
                                tmpdata.paste(v.data)
                                results[k]=content(tmpdata,v.lenx,newy)
                        self.act_redraw(stored=True,act_index=act_index)
                        self.further_act_ctrl(act_name, act_index)
                        self.redraw()
                        win2.destroy()
                    def act_reset():
                        for part in ctrl_key:
                            self.selections[part][2]=[0,0]
                        self.act_redraw()
                    def base_mirror_handler():
                        if self.basemirrored:
                            self.basemirrored=False
                        else:
                            self.basemirrored=True
                        self.act_redraw()

                    btn_frame=tk.Frame(left_frame)
                    btn_frame.pack(pady=5)
                    save_btn = tk.Button(btn_frame, text="저장", command=save_and_close).grid(row=0, column=0, padx=5)
                    reset_btn = tk.Button(btn_frame, text="위치초기화", command=act_reset).grid(row=0, column=1, padx=5)
                    mirror_btn=tk.Button(btn_frame, text="몸/바지 반전", command=base_mirror_handler).grid(row=0, column=2, padx=5)

                    def make_handler(p):
                        def handler(event):
                            self.last_selected_part=p
                            if self.isfix:
                                if p=="피부" or p=="바지":  #팔피부바지 고정기능
                                    value=int(self.selections[p][1].get())
                                    value2=(value//6)*12+(value%6)
                                    self.selections["팔"][1].set(value2)
                                    self.selections["피부"][1].set(value)
                                    self.selections["바지"][1].set(value)
                                elif p=="팔":
                                    value=int(self.selections[p][1].get())
                                    value2=(value//12)*6+value%6
                                    check=value%12
                                    if check>=6:
                                        if check<9:
                                            value2=(value//12+1)*6+value%6
                                            value=((value//12)+1)*12+(value%6)
                                        else:
                                            value=((value//12))*12+(value%6)
                                    if value==252:
                                        value=0;value2=0;
                                    self.selections["팔"][1].set(value)
                                    self.selections["피부"][1].set(value2)
                                    self.selections["바지"][1].set(value2)
                            self.act_redraw()
                            self.act_canvas.focus_set()
                        return handler
                    # 콤보박스 선택 시
                    for part in self.selections:
                        option, widgets, _,_ =self.selections[part]
                        if option:
                            option.bind("<<ComboboxSelected>>", make_handler(part))
                        widgets.bind("<<ComboboxSelected>>", make_handler(part))

                    # 화살표 키로 좌표 조정
                    def move_selection(event):
                        if not self.last_selected_part:
                            return  # 선택된 항목이 없다면 무시
                        key = ctrl_key[self.last_selected_part]
                        dx, dy = 0, 0
                        if event.keysym == "Left":
                            dx = -1
                        elif event.keysym == "Right":
                            dx = 1
                        elif event.keysym == "Up":
                            dy = -1
                        elif event.keysym == "Down":
                            dy = 1
                        else:
                            return
                        # 좌표 수정
                        self.selections[self.last_selected_part][2][0] += dx
                        self.selections[self.last_selected_part][2][1] += dy
                        self.act_redraw()
                    self.act_canvas.bind("<KeyPress>", move_selection)
                    self.act_canvas.focus_set()

                    self.act_redraw() #추가 액션 에딧 창
                # 선택값을 기반으로 미리보기 재조립
                def act_redraw(self, stored=False, act_index=None):
                        base = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
                        self.new_shirt.clear()
                        for part in self.layers_Korean:
                            tmp=contents[self.ctrl_key[part]]
                            sel = self.selections[part]
                            sel[3]=False
                            #머리 헤어 등 앞뒤옆 배치
                            if sel[1].get()=="없음":
                                token=Image.new("RGBA", (1, 1), (0, 0, 0, 0))
                                if part=="셔츠":
                                    for i in range(3):
                                        self.new_shirt.append(skincolors[2-i])
                            else:
                                if sel[0]: #기본 등의 옵션 셀렉트가 존재한다면
                                    option=sel[0].get() #첫번째, 바지 모양을 고를 수 있는 콤보박스
                                    if part=="바지":
                                        optiond=sel[1].get() #두번째, 바지 동작을 고를 수 있는 콤보박스
                                        optiond=int(optiond)
                                        if option=="기본":
                                            row=(optiond//self.ctrl_index[part][0])
                                            col=(optiond%self.ctrl_index[part][0])
                                            if gender=="Female":
                                                col+=6
                                            self.base_ref[part]=(row,col)
                                            token = tmp.index(row+pants[1], col+pants[0])
                                        else:
                                            option=int(option)
                                            addrow=21*(option//10)
                                            addcol=12*(option%10)
                                            row=(optiond//self.ctrl_index[part][0])+addrow
                                            col=(optiond%self.ctrl_index[part][0])+addcol
                                            if gender=="Female":
                                                col+=6
                                            token = tmp.index(row, col)

                                        token=multiply_color_preserve_transparency(token, pickcolor[2])
                                        if self.basemirrored:
                                            token=ImageOps.mirror(token)
                                            sel[3]=True
                                    else:
                                        optiond=int(self.ctrl_index[part].index(sel[1].get())) #앞뒤옆
                                        if option=="기본": #기본이라면
                                            if part=="셔츠": 
                                                token=shirts[optiond] 
                                            elif part=="악세서리":
                                                if optiond==2:
                                                    token=ImageOps.mirror(accs[1])
                                                    sel[3]=True
                                                else:
                                                    token=accs[optiond]
                                            elif part=="헤어":
                                                try:
                                                    token=hairs[optiond]
                                                except:
                                                    token=ImageOps.mirror(hairs[1])
                                                    sel[3]=True
                                            elif part=="모자":
                                                token=hats[optiond]
                                        else:
                                            option=int(option)
                                            if part=="헤어":
                                                if option<56: #헤어스타일 1
                                                    if optiond==3:
                                                        token=ImageOps.mirror(tmp.index((option//tmp.lenx)*3+1, option%tmp.lenx))
                                                        sel[3]=True
                                                    else:
                                                        token=tmp.index((option//tmp.lenx)*3+optiond, option%tmp.lenx)
                                                else: #헤어스타일 2
                                                    token=tmp.index(21+((option-56)//tmp.lenx)*4+optiond, option%tmp.lenx)
                                                token=multiply_color_preserve_transparency(token, pickcolor[1])
                                            elif part=="악세서리":
                                                if optiond==2:
                                                    token=ImageOps.mirror(tmp.index((option//tmp.lenx)*2+1, option%tmp.lenx))
                                                    sel[3]=True
                                                else:
                                                    token=tmp.index((option//tmp.lenx)*tmp.num+optiond, option%tmp.lenx)
                                                if option<=5 or (19<=option and option<=22):
                                                    token=multiply_color_preserve_transparency(token, pickcolor[1])
                                            else:
                                                token=tmp.index((option//tmp.lenx)*tmp.num+optiond, option%tmp.lenx)
                                                if part=="셔츠":
                                                    self.new_shirt.append(tmp.index((option//tmp.lenx)*tmp.num, option%tmp.lenx).getpixel((0,2)))
                                                    self.new_shirt.append(tmp.index((option//tmp.lenx)*tmp.num, option%tmp.lenx).getpixel((0,3)))
                                                    self.new_shirt.append(tmp.index((option//tmp.lenx)*tmp.num, option%tmp.lenx).getpixel((0,4)))
                                else:
                                    option=int(sel[1].get())
                                    if part=="팔":
                                        row=option//self.ctrl_index[part][0]
                                        col=option%self.ctrl_index[part][0]+6
                                        self.base_ref[part]=(row,col)
                                        token = tmp.index(row, col)
                                        if self.new_shirt:
                                            token=replace_color(token,(142,31,12,255),self.new_shirt[0],skincolors)
                                            token=replace_color(token,(112,23,24,255),self.new_shirt[1],skincolors)
                                            token=replace_color(token,(74,12,6,255),self.new_shirt[2],skincolors)
                                        else:
                                            token=replace_color(token,(142,31,12,255),shirts[0].getpixel((0,2)),skincolors)
                                            token=replace_color(token,(112,23,24,255),shirts[0].getpixel((0,3)),skincolors)
                                            token=replace_color(token,(74,12,6,255),shirts[0].getpixel((0,4)),skincolors)
                                        for i in range(3):
                                            token=replace_color(token,basecolors[i],skincolors[i])
                                    elif part=="피부":
                                        row=option//self.ctrl_index[part][0]
                                        col=option%self.ctrl_index[part][0]
                                        self.base_ref[part]=(row,col)
                                        token = tmp.index(row, col)
                                        token=replace_color(token,(85, 0, 0, 255),shoecolors[0])
                                        token=replace_color(token,(91,31,36,255),shoecolors[1])
                                        token=replace_color(token,(119,41,26,255),shoecolors[2])
                                        token=replace_color(token,(173,71,27,255),shoecolors[3])
                                        for i in range(3):
                                            token=replace_color(token,basecolors[i],skincolors[i])
                                        token=replace_color(token,(104, 43, 15, 255),pickcolor[0])
                                    if self.basemirrored:
                                        token=ImageOps.mirror(token)
                                        sel[3]=True
                            if stored:
                                basetmp=results["base"]
                                x_global=(act_index%basetmp.lenx)*basetmp.tokenx+sel[2][0]
                                y_global=(act_index//basetmp.lenx)*basetmp.tokeny+sel[2][1]
                                if sel[0]: #기본 등의 옵션 셀렉트가 존재한다면
                                    option=sel[0].get()
                                    if part=="바지":
                                        key=self.ctrl_key[part]
                                        if option=="기본":
                                            results[key].data.paste(token,(x_global,y_global))
                                        else:
                                            tmpdata=Image.new("RGBA", (basetmp.getx, basetmp.gety), (0, 0, 0, 0))
                                            tmpdata.paste(token,(x_global,y_global))
                                            results[key+sel[0].get()]=content(tmpdata,basetmp.lenx,basetmp.leny)
                                    elif option=="기본":
                                        results[self.ctrl_key[part]].data.paste(token,(x_global,y_global))
                                    else:
                                        tmpdata=Image.new("RGBA", (basetmp.getx, basetmp.gety), (0, 0, 0, 0))
                                        tmpdata.paste(token,(x_global,y_global))
                                        results[self.ctrl_key[part]+sel[0].get()]=content(tmpdata,basetmp.lenx,basetmp.leny)
                                else:
                                    if part=="팔":
                                        key="arms"
                                    else: key=self.ctrl_key[part]
                                    results[key].data.paste(token,(x_global,y_global))
                            else: base.paste(token, tuple(sel[2]), token)
                        base = base.resize(self.act_canvas_size, resample=Image.NEAREST)
                        img = ImageTk.PhotoImage(base)
                        self.act_canvas.delete("all")
                        self.act_canvas.create_image(0, 0, anchor="nw", image=img)
                        self.act_canvas.image = img
                def sort_key(self,s):
                    for i,v in enumerate(self.layers_English):
                        if s.startswith(v):
                            return (i,s)
                    return (len(self.layers_English),s)                   
                def redraw(self): #select에 담긴 값을 바탕으로 result dict에 해당되는 토큰 조립하여 추가하고
                    base = Image.new("RGBA", results["base"].data.size,(0,0,0,0))
                    for key in sorted(results.keys(),key=self.sort_key): 
                        base.paste(results[key].data,(0,0),results[key].data)
                    if self.canvas_channel==0:
                        self.canvas_size=(800//results["base"].leny,400)
                        base=base.resize(self.canvas_size, resample=Image.NEAREST)
                        # PIL → PhotoImage 변환 후 캔버스에 표시
                        self.tk_img = ImageTk.PhotoImage(base)
                        self.canvas.delete("all")
                        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
                        if hasattr(self, 'after_id'):
                            self.canvas.after_cancel(self.after_id)
                            del self.after_id
                            self.anim_index = 0  # 선택적으로 초기화
                    else: #채널이 있으면
                        if not hasattr(self, "anim_index"):
                            self.anim_index = 0
                        else:
                            self.anim_index = (self.anim_index + 1) % 4  # 프레임 인덱스 0~3 루프
                        # 16x32 단위로 애니메이션 프레임 선택
                        x1 = 16 * self.anim_index
                        y1 = 32 * (self.canvas_channel - 1)
                        x2 = x1 + 16
                        y2 = y1 + 32
                        cropped = base.crop((x1, y1, x2, y2))
                        self.canvas_size=(200,400)
                        base = cropped.resize(self.canvas_size, resample=Image.NEAREST)

                        self.tk_img = ImageTk.PhotoImage(base)
                        self.canvas.delete("all")
                        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

                        # 0.5초 후 다시 redraw 실행 (애니메이션 루프)
                        self.after_id=self.canvas.after(500, self.redraw)
                def export_png(self): #병합한 이미지를 콤보박스의 내용에 따라 이름이 정해지고 저장함 content에 append도
                    base = Image.new("RGBA", results["base"].data.size,(0,0,0,0))
                    for key in sorted(results.keys(),key=self.sort_key): 
                        base.paste(results[key].data,(0,0),results[key].data)
                    category = self.season_combo.get()
                    upload_img(category, base, "sprites")
        
        CharacterCreator(win)
    def load_sprite(): #애니메이션 매니저로 txt파일 편집할 수 있어야함 결혼가능일경우 자동 삽입도
        win = tk.Toplevel(root)
        win.title("스프라이트 불러오기")
        win.geometry("300x180")
        tk.Label(win, text="스프라이트 종류").pack(pady=10)
        season_combo = ttk.Combobox(win, values=["default", "spring", "summer", "fall", "winter","beach"], width=15)
        season_combo.pack()
        season_combo.set("default")

        # 업로드 핸들러 함수
        def upload():
            category = season_combo.get()
            file_path = filedialog.askopenfilename(title="스프라이트 선택", filetypes=[("PNG 이미지", "*.png"), ("모든 파일", "*.*")])
            if not file_path:
                return  # 사용자가 파일 선택 안 한 경우
            try:
                img = Image.open(file_path)
            except Exception as e:
                tk.messagebox.showerror("오류", f"이미지 열기 실패: {e}")
                return
            imgx,imgy=img.size
            if imgx%16 or imgy%32: #이미지 크기 x 는16, y가 32로 나누어떨어지지 않으면 오류 메시지
                tk.messagebox.showerror("오류", "잘못된 형식입니다")
                return
            upload_img(category, img, "sprites")
            spriteaction_manager(img)
            win.destroy()  
        tk.Button(win, text="업로드", command=upload).pack(pady=20)
    def choose_load_or_open_sprite():
        win = tk.Toplevel(root)
        win.title("스프라이트 생성 또는 불러오기")
        win.geometry("300x150")
        def one():
            open_sprite_generator()
            win.destroy()
        def two():
            load_sprite()
            win.destroy()
        tk.Button(win, text="생성", command=one).pack(pady=20)
        tk.Button(win, text="불러오기", command=two).pack(pady=20)
    #선물맛구현
    def open_gift_preferences():
        win = tk.Toplevel(root)
        win.title("선물 선호도")
        main = tk.Frame(win)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        class ToolTip:
            def __init__(self, widget, text):
                self.widget = widget
                self.text   = text
                self.tipwin = None
                widget.bind("<Enter>", self.show)
                widget.bind("<Leave>", self.hide)
            def show(self, _e):
                if self.tipwin or not self.text:
                    return
                x, y, cx, cy = self.widget.bbox("insert")
                x += self.widget.winfo_rootx() + 25
                y  = self.widget.winfo_rooty() + 20
                self.tipwin = tw = tk.Toplevel(self.widget)
                tw.wm_overrideredirect(True)
                tw.wm_geometry(f"+{x}+{y}")
                label = tk.Label(tw, text=self.text, justify="left",
                                 background="#ffffe0", relief="solid", borderwidth=1,
                                 font=("맑은고딕", "10", "normal"))
                label.pack(ipadx=1)
            def hide(self, _e):
                if self.tipwin:
                    self.tipwin.destroy()
                    self.tipwin = None
        # 드래그용 데이터
        _drag_data = {
            "widget":   None,
            "name":     None,
            "image":    None,
            "offset_x": 0,
            "offset_y": 0,
            "floating": None,
            "root_x":   0,
            "root_y":   0,
        }
        def on_drag_start(event):
            lbl = event.widget
            # 드래그 대상 위젯과 이름, 이미지 저장
            _drag_data["widget"] = lbl
            _drag_data["name"]   = lbl._item_name   # 라벨 생성 시 lbl._item_name = k 로 저장해 두었다고 가정
            _drag_data["image"]  = getattr(lbl, "image", None)
    
            # 토탈 윈도우 좌표 기준
            parent = lbl.winfo_toplevel()
            _drag_data["root_x"] = parent.winfo_rootx()
            _drag_data["root_y"] = parent.winfo_rooty()
    
            # 뜨는 Label 생성
            floating = tk.Label(parent,
                                image=_drag_data["image"],
                                bd=1, relief="solid")
            _drag_data["floating"] = floating
    
            # 마우스 좌표 기준 place 위치 계산
            x = event.x_root - _drag_data["root_x"]
            y = event.y_root - _drag_data["root_y"]
            floating.place(x=x, y=y)    
        def on_drag_motion(event):
            floating = _drag_data.get("floating")
            if not floating:
                return
            x = event.x_root - _drag_data["root_x"]
            y = event.y_root - _drag_data["root_y"]
            floating.place(x=x, y=y)   
        def on_drag_release(event):
            floating = _drag_data.get("floating")
            if not floating:
                return
            # 드롭한 마우스 절대 좌표
            x_abs, y_abs = event.x_root, event.y_root
            drag_data_name=_drag_data["name"]
            duplicate=False
            for emo, frame, listbox in drop_zones:
                if drag_data_name in listbox.get(0,tk.END): #어떤 리스트박스든 중복되는 이름이 존재하면
                    messagebox.showerror("중복",f"{emo} 박스에 {drag_data_name}(이)가 이미 존재합니다")
                    duplicate=True
            if not duplicate:
                for emo, frame, listbox in drop_zones:
                    x1 = frame.winfo_rootx()
                    y1 = frame.winfo_rooty()
                    x2 = x1 + frame.winfo_width()
                    y2 = y1 + frame.winfo_height()
                    if x1 < x_abs < x2 and y1 < y_abs < y2:
                        # 리스트박스에 _drag_data["name"] 을 추가
                        listbox.insert(tk.END, drag_data_name)
                        break
            # floating 레이블 제거
            floating.destroy()
            # 데이터 초기화
            for k in ("widget","name","image","floating"):
                _drag_data[k] = None
        def on_double_click(event, idx):
            listbox=drop_zones[idx][2]
            selection=listbox.curselection()
            if selection:
                index=selection[0]
                listbox.delete(index)

        # ── 왼쪽: 아이콘 스크롤 프레임 ─────────────────────
        icon_container = tk.Frame(main)
        icon_container.grid(row=0, column=0, sticky="nsw")
        
        canvas = tk.Canvas(icon_container, width=50, height=400)
        scroll = tk.Scrollbar(icon_container, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="y")
        scroll.pack(side="right", fill="y")
        canvas.create_window((0,0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        #아이템들 추가
        for k,v in sd_items.items():
            icon_path=os.path.join(os.getcwd(), "content", "stardew_items", v.english+".png")
            if os.path.isfile(icon_path):
                img = Image.open(icon_path).resize((32,32), Image.LANCZOS)
                photo=ImageTk.PhotoImage(img)
                lbl = tk.Label(inner, image=photo, bd=1, relief="raised") 
            else:
                lbl = tk.Label(inner, text=k[:-5],bd=1, relief="raised")
                photo=None
            lbl.image = photo
            lbl._item_name = k
            lbl.pack(padx=4, pady=4)
            ToolTip(lbl, k)
            lbl.bind("<Button-1>",      on_drag_start)
            lbl.bind("<B1-Motion>",     on_drag_motion)
            lbl.bind("<ButtonRelease-1>", on_drag_release)

        def edit_gift_text(i):
            seq=(0,2,8,4,6)
            chars[seq[i]]=open_text_editor(chars[seq[i]])

        # ── 중간: 5개의 드롭 존 ─────────────────────────
        drop_frame = tk.Frame(main)
        drop_frame.grid(row=0, column=1, padx=20, sticky="n")
        emotions = ["사랑", "좋아", "중립", "싫어", "혐오"]
        drop_zones = []     
        for i, emo in enumerate(emotions):
            lf = tk.LabelFrame(drop_frame, text=emo, labelanchor="n", width=200, height=80)
            lf.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
            plusbtn=tk.Button(drop_frame, text="+대사", command=lambda idx=i: edit_gift_text(idx))
            plusbtn.grid(row=i, column=1, padx=5, pady=5)
            # 내부에 Listbox
            lb = tk.Listbox(lf, height=4, width=20)
            lb.bind("<Double-Button-1>", lambda event, idx=i: on_double_click(event, idx))
            lb.pack(fill="both", expand=True, padx=4, pady=4)
            drop_zones.append((emo, lf, lb))
        tk.Label(win,text="이것은 개인적인 선호도를 결정짓는 작업이기 때문에\n아이템 전부를 분류할 필요는 없습니다. 보편적인 취향에 대해서는\nstardewvalleywiki.com/List_of_All_Gifts를 참조\n우선순위 (개인 선호 아이템>개인 선호 범주>보편적 취향)").pack(padx=5, pady=10)
        # ── 오른쪽: 저장/설명 라벨  ─────────────────────────
        save_frame = tk.Frame(main)
        save_frame.grid(row=0, column=2, padx=10, sticky="n")
        def gift_data_save():
            ids_seq=(1,3,9,5,7)
            for i,(_,_,box) in enumerate(drop_zones):
                chars[ids_seq[i]]=""
                for item_name in box.get(0,tk.END):
                    for key,val in sd_items.items():
                        if item_name==key:
                            chars[ids_seq[i]]+=str(val.id)
                            chars[ids_seq[i]]+=" "
                chars[ids_seq[i]]=chars[ids_seq[i]][:-1]
            gift_result=""
            for i in range(0,10,2):
                gift_result+=(chars[i]+"/")
                gift_result+=(chars[i+1]+"/")
            result["Entries"][characterID]=gift_result
            append_to_content(result, data, modify_to_index)
            win.destroy()
        savebtn=tk.Button(save_frame, text="저장", command=gift_data_save)
        savebtn.grid(row=0, column=0, pady=5)
        tk.Label(save_frame,text="드래그로\n항목 추가,\n삭제는\n더블클릭").grid(row=1,column=0)

        #불러오기, 없다면 데이터 생성(그러나 저장을 누르기 전까지는 append되지 않음)
        data = load_content_json(project_dir)
        result={
                "Action": "EditData",
                "Target": "Data/NPCGiftTastes",
                "Entries": {
		            characterID: ""
                 }
            }
        modify_to_index=is_existing_data(result, data) 
        if modify_to_index:
            try:
                result=data["Changes"][modify_to_index]
                #텍스트로 저장된 선물취향을 listbox에 재배치 구현
                chars=result["Entries"][characterID][:-1].split("/")
                for i, index in enumerate((1,3,9,5,7)):
                    ids=chars[index].split(" ")
                    if not ids==[""]:
                        for id in ids:
                            for k,v in sd_items.items():
                                if (v.id==int(id)):
                                    drop_zones[i][2].insert(tk.END, k)

            except Exception:
                messagebox.showerror("오류", "선물 취향을 불러올 수 없습니다.")
                return None
        else: #디폴트 대사
            chars=["이거 진짜 좋다! @, 너가 최고야!","",
                   "오. 나 지금 배고픈 거 어떻게 알았어? 맛있겠다!","",
                   "...응? 왜?","",
                   "더러워!","",
                   "선물이구나? 고마워.",""]
    def open_dialogue_editor():
        win = tk.Toplevel(root)
        title = "다이얼로그 생성"
        win.title(title)
        win.geometry("900x600")
        notebook = ttk.Notebook(win)
        notebook.pack(expand=True, fill='both')
        tab=[]
        festival_key={"품평회 심사 중":"Fair_Judging","품평회에 보라색바지 전시":"Fair_Judged_PlayerLost_PurpleShorts",
                      "품평회에 아무것도 놓지않음":"Fair_Judged_PlayerLost_Skipped","품평회에서 (농부가) 1등하지 못함":"Fair_Judged_PlayerLost",
                      "품평회에서 농부가 이김":"Fair_Judged_PlayerWon","품평회 심사 후 기본 대사":"Fair_Judged",
                      "플라워댄스수락(룸메이트일경우)":"FlowerDance_Accept_Roommate","플라워댄스수락(배우자일경우)":"FlowerDance_Accept_Spouse",
                      "플라워댄스수락":"FlowerDance_Accept","플라워댄스 거절":"FlowerDance_Decline","겨울별축제(선물열기전,룸메)":"WinterStar_GiveGift_Before_Roommate",
                      "겨울별축제(선물열기전,배우자)":"WinterStar_GiveGift_Before_Spouse","겨울별축제(선물 열기 전)":"WinterStar_GiveGift_Before",
                      "겨울별축제(선물연후,룸메)":"WinterStar_GiveGift_After_Roommate","겨울별축제(선물연후,배우자)":"WinterStar_GiveGift_After_Spouse",
                      "겨울별축제(선물 연 후)":"WinterStar_GiveGift_After"
                      }
        item_d_key={"생일선물받기(싫은것)":"AcceptBirthdayGift_Negative","생일선물받기(좋은것또는중립)":"AcceptBirthdayGift_Positive","생일선물받기":"AcceptBirthdayGift",
                    "꽃다발 받을 때":"AcceptBouquet","선물받기":"AcceptGift","영화관 초대 반응":"MovieInvitation","꽃다발거부(연애불가)":"RejectBouquet_NotDatable",
                    "꽃다발거부(딴사람과결혼함)":"RejectBouquet_NpcAlreadyMarried","꽃다발거부(이미수락약혼)":"RejectBouquet_AlreadyAccepted_Engaged",
                    "꽃다발거부(이미수락결혼)":"RejectBouquet_AlreadyAccepted_Married","꽃다발거부(이미수락)":"RejectBouquet_AlreadyAccepted",
                    "꽃다발거부(농부와이혼)":"RejectBouquet_Divorced","꽃다발거부(하트4미만)":"RejectBouquet_VeryLowHearts","꽃다발거부(하트8미만)":"RejectBouquet_LowHearts",
                    "꽃다발거부":"RejectBouquet","선물거부(농부와이혼)":"RejectGift_Divorced","인어펜던트거부(이미수락약혼)":"RejectMermaidPendant_AlreadyAccepted_Engaged",
                    "인어펜던트거부(이미수락결혼)":"RejectMermaidPendant_AlreadyAccepted_Married","인어펜던트거부(이미수락)":"RejectMermaidPendant_AlreadyAccepted","인어펜던트거부(농부와이혼)":"RejectMermaidPendant_Divorced",
                    "인어펜던트거부(집업그레이드필요)":"RejectMermaidPendant_NeedHouseUpgrade","인어펜던트거부(로맨스불가)":"RejectMermaidPendant_NotDatable","인.펜거부(NPC가딴사람과결혼)":"RejectMermaidPendant_NpcWithSomeoneElse",
                    "인.펜거부(농부가딴사람과결혼)":"RejectMermaidPendant_PlayerWithSomeoneElse","인어펜던트거부(하트8미만)":"RejectMermaidPendant_Under8Hearts","인어펜던트거부(하트10미만)":"RejectMermaidPendant_Under10Hearts",
                    "인.펜거부(♥10미만,거절후재시도)":"RejectMermaidPendant_Under10Hearts_AskedAgain","인어펜던트거부":"RejectMermaidPendant","영화거부(다른사람에게초대됨)":"RejectMovieTicket_AlreadyInvitedBySomeoneElse",
                    "영화거부(이번주에이미봄)":"RejectMovieTicket_AlreadyWatchedThisWeek","영화거부(농부와이혼)":"RejectMovieTicket_Divorced","영화거부(NPC설정에의해)":"RejectMovieTicket_DontWantToSeeThatMovie",
                    "영화티켓거부":"RejectMovieTicket","룸메제안거부(이미수락)":"RejectRoommateProposal_AlreadyAccepted","룸메제안거부(NPC가이미있음)":"RejectRoommateProposal_NpcWithSomeoneElse",
                    "룸메제안거부(농부가이미있음)":"RejectRoommateProposal_PlayerWithSomeoneElse","룸메제안거부(하트10미만)":"RejectRoommateProposal_LowFriendship","룸메제안거부(집이작음)":"RejectRoommateProposal_SmallHouse","룸메제안거부":"RejectRoommateProposal"
                    }
        unique_key={"이별통보받으면":"breakUp","이혼후말걸면":"divorced","쓰레기통뒤지는거봄":"DumpsterDiveComment","녹색비(1년차)이벤트중":"GreenRain",
                    "녹색비(2년차)이벤트중":"GreenRain_2","농부에게새총으로쏘임":"HitBySlingshot","리조트":"Resort","리조트 바":"Resort_Bar","리조트 의자":"Resort_Chair",
                    "리조트 댄스":"Resort_Dance","리조트 입장":"Resort_Entering","리조트 퇴장":"Resort_Leaving","리조트 해변":"Resort_Shore","리조트 타월":"Resort_Towel",
                    "리조트 우산":"Resort_Umbrella","리조트 돌아다니기":"Resort_Wander","결혼 후 주방을 못 찾을 때":"SpouseFarmhouseClutter","결혼 후 타NPC 선물 질투":"SpouseGiftJealous","결혼후 농장근처 몬스터존재":"Spouse_MonstersInHouse",
                    "별방울(stardrop)을 주며":"SpouseStardrop","기억삭제 후 처음대화":"WipedMemory"
                    }
        marriged_key={"농장을 나갈때":"funLeave","직장갈때(보통미사용)":"jobLeave","1시이후농장들어오는중만나면":"funReturn","직장에서돌아오는중(보통미사용)":"jobReturn",
                      "봄에 하트9이상이면 5%로":"spring","여름에 하트9이상이면 5%로":"summer","가을에 하트9이상이면 5%로":"fall","겨울에 하트9이상이면 5%로":"winter",
                      "농장에서 20%로":"Outdoor","자신의 방에서":"spouseRoom","파티오에서":"patio"
                      }
        marriged_key={k:v+"_"+load_unique_id() for k,v in marriged_key.items()}
        Affection={"애정:나쁨":"Bad","애정:중립":"Neutral","애정:좋음":"Good"}
        event_dial_key={"농부가 생성될 때(6 days)":"Introduction","처음으로 연못에 게 10마리가 있음(14 days)":"FullCrabPond","1년차 그린 레인이 끝남(2 days)":"GreenRainFinished","플레이어가 NPC와 처음으로 데이트(4 days)":"dating",
                        "플레이어가 NPC와 처음으로 결혼(4 days)":"married","플레이어가 NPC와 두 번째로 결혼(4 days)":"married_twice","플레이어가 처음으로 이혼(4 days)":"divorced_once","플레이어가 두 번째로 이혼(4 days)":"divorced_twice","팸의 집 업그레이드(기부자로 밝혀진 경우)(4 days)":"pamHouseUpgrade",
                        "팸의 집 업그레이드(익명 기부)(4 days)":"pamHouseUpgradeAnonymous","윌리6하트이벤트(4 days)":"willyCrabs","플렝이어가 처음으로 달걀 찾기 우승(4 days)":"wonEggHunt","플레이어가 처음으로 그랜지디스플레이쇼케이스 우승(4 days)":"wonGrange",
                        "플레이어가 처음으로 얼음 낚시 대회 우승(4 days)":"wonIceFishing","센터에서 주니모 메모를 읽음(4 days)":"cc_Begin","커뮤니티 센터를 완료함(4 days)":"cc_Complete","산 바위가 제거됨(7 days)":"cc_Boulder","채석장 다리가 수리됨(7 days)":"cc_Bridge",
                        "버스가 수리됨(7 days)":"cc_Bus","온실이 건설됨(3 days)":"cc_Greenhouse","광산 카트 잠금 해제됨(7 days)":"cc_Minecart","처음 조자 커뮤니티 개발 양식을 염(7 days)":"joja_Begin","영화관 건설됨(3 days)":"movieTheater",
                        "엘리엇14하트이벤트(6 days)":"elliottGone","엘리엇14하트이벤트1":"ElliottGone1","엘리엇14하트이벤트2":"ElliottGone2","엘리엇14하트이벤트3":"ElliottGone3","엘리엇14하트이벤트4":"ElliottGone4",
                        "엘리엇14하트이벤트5":"ElliottGone5","엘리엇14하트이벤트6":"ElliottGone6","엘리엇14하트이벤트7":"ElliottGone7","에밀리14하트이벤트(2 days)":"emilyFiber","헤일리14하트이벤트1":"haleyCakewalk1","헤일리14하트이벤트2":"haleyCakewalk2",
                        "레아14하트이벤트":"leahPaint","페니14하트이벤트2(2 days)":"pennyRedecorating","샘14하트이벤트1(2 days)":"samJob1","샘14하트이벤트2":"samJob2","샘14하트이벤트3(3 days)":"samJob3","세바스찬14하트이벤트":"sebastianFrog","세바스찬14하트이벤트2(6 days)":"sebastianFrog2","셰인14하트이벤트1":"shaneSaloon1","셰인14하트이벤트2":"shaneSaloon2",
                        "첫번째애완동물입양(4 days)":"gotPet","10하트그룹이벤트_남자들(7 days)":"dumped_Guys","10하트그룹이벤트_여자들":"dumped_Girls","10하트_두번째기회 여자들(14 days)":"secondChance_Girls","10하트_두번째기회 남자들":"secondChance_Guys",
                        "첫 번째 집 업그레이드(4D)":"houseUpgrade_1","두 번째 집 업그레이드(4D)":"houseUpgrade_2","세 번째 집 업그레이드(4D)":"houseUpgrade_3",
                        "처음으로 광산 1~10층 들어감(4D)":"mineArea_0","처음으로 광산 11~39층 들어감(4D)":"mineArea_10","처음으로 광산 40~79층 들어감(4D)":"mineArea_40","처음으로 광산 80~120층 들어감(4D)":"mineArea_80","처음으로 광산 해골동굴층 들어감(4D)":"mineArea_121","처음으로 광산 채석장광산 들어감(4D)":"mineArea_77377",
                        "처음으로 닭 구매(4D)":"purchasedAnimal_Chicken","처음으로 오리 구매(4D)":"purchasedAnimal_Duck","처음으로 토끼 구매(4D)":"purchasedAnimal_Rabbit","처음으로 공룡 구매(4D)":"purchasedAnimal_Dinosaur","처음으로 소 구매(4D)":"purchasedAnimal_Cow",
                        "처음으로 염소 구매(4D)":"purchasedAnimal_Goat","처음으로 양 구매(4D)":"purchasedAnimal_Sheep","처음으로 돼지 구매(4D)":"purchasedAnimal_Pig","처음으로 타조 구매(4D)":"purchasedAnimal_Ostrich",
                        "처음 건설 주니모 오두막(4D)":"structureBuilt_Junimo Hut","처음 건설 골드 시계(4D)":"structureBuilt_Gold Clock","처음 건설 닭장(4D)":"structureBuilt_Coop","처음 건설 헛간(4D)":"structureBuilt_Barn",
                        "처음 건설 우물(4D)":"structureBuilt_Well","처음 건설 저장고(4D)":"structureBuilt_Silo","처음 건설 제분기(4D)":"structureBuilt_Mill","처음 건설 헛간(4D)":"structureBuilt_Shed",
                        "처음 건설 물고기 연못(4D)":"structureBuilt_Fish Pond","처음 건설 오두막(4D)":"structureBuilt_Cabin","처음 건설 반려동물 그릇(4D)":"structureBuilt_Pet Bowl","처음 건설 마구간(4D)":"structureBuilt_Stable","처음 건설 슬라임장(4D)":"structureBuilt_Slime Hutch",
                        "처음 건설 배송 상자(4D)":"structureBuilt_Shipping Bin","처음 건설 농장(4D)":"structureBuilt_Farmhouse","처음 건설 온실(4D)":"structureBuilt_Greenhouse"
                        }
        event_withNPC={"처음으로 데이트":"dating_","처음으로 이혼":"divorced_","처음으로 결혼":"married_","처음으로 룸메이트":"roommates_"}
        taste={"사랑/사랑하는":"_Loved", "좋아하는":"_Liked","중립선호도":"_Neutral","싫어하는":"_Disliked","혐오하는":"_Hated"}
        TheDayAfter={"-":"","하루가 지남":"_memory_oneday","일주일이 지남":"_memory_oneweek","2주가 지남":"_memory_twoweeks","4주가 지남":"_memory_fourweeks","8주가 지남":"_memory_eightweeks","1년이 지남":"_memory_oneyear"}
        event_withObj={"처음으로 물고기":"fishCaught","처음으로 완전히 자란 작물":"cropMatured"}
        event_info=load_event_info(); event_info={b:c for a,b,c in event_info}

        Integration={k:v+"_" for k,v in Season.items()}|{"1년차":"_1","그 이후":"_2"}|{Name + "와 결혼": "_inlaw_"+Name for Name in NPCName}
        Integration=Integration|{str(num)+"일":str(num) for num in range(1,29)}|{k:"_"+v for k,v in DayOfWeek.items()}|{k+"요일":v for k,v in DayOfWeek.items()}
        Integration=Integration|{k+" 호감도"+str(num):v+str(num) for k,v in DayOfWeek.items() for num in range(2,11,2)}
        Integration=Integration|{str(num)+"하트":str(num) for num in range(2,11,2)}|{"겨울별축제 선물반응":"WinterStar_ReceiveGift"}
        Integration=Integration|festival_key|{k:"_(O)"+str(v.id) for k,v in sd_items.items() if v.id>0}|{k:"_"+v.english for k,v in sd_items.items() if v.id<0}
        Integration=Integration|taste|item_d_key|{"특정선물거부":"RejectItem"}|unique_key|marriged_key|Affection|{str(num)+"번 대사":"_"+str(num-1) for num in range(1,11)}|{"0번 대사":"_"+load_unique_id()}
        Integration=Integration|{"비 오는 날":"Rainy_Day", "비 안 오는 날 또는 실내":"Indoor_Day","비 내리는 저녁 농가":"Rainy_Night","비 안 오는 저녁 농가":"Indoor_Night","농장에서 80%로":"Outdoor","부엌에서(자녀 한 명인 경우)":"OneKid","부엌에서(자녀 두 명인 경우)":"TwoKids"}
        Integration=Integration|event_dial_key|TheDayAfter|event_withNPC|{k+"을(를)":"_"+str(v.id) for k,v in sd_items.items() if v.id>0}|event_withObj|{"처음으로 이벤트":"eventSeen_","처음으로 장소":"firstVisit_","처음으로 업적 (id: ":"achievement_","처음으로 퀘스트 (id: ":"questComplete_"}|event_info|{"-":""}


        def generate_dialogue_items(current,Rkey=None):
            new_items={}
            indexj=0
            mb_visited=False
            for frame in current.winfo_children():
                if isinstance(frame,tk.Frame):
                    for row in frame.winfo_children():
                        if isinstance(row,tk.Frame):
                            value=[]
                            valid=True
                            for widget in row.winfo_children():
                                if isinstance(widget,ttk.Combobox):
                                    if widget not in value:
                                        value.append(widget)
                                elif isinstance(widget,tk.Entry):
                                    dial=widget.get()
                                    if not dial:
                                        if not mb_visited:
                                            messagebox.showinfo("안내","대사가 공백인 행은 추가되지 않습니다")
                                            mb_visited=True
                                        valid=False
                            

                            for i in range(len(value)):
                                key=value[i].get()
                                if Rkey==None:
                                    if not key:
                                        if not mb_visited:
                                            messagebox.showinfo("안내","공백이 존재하는 행은 추가되지 않습니다")
                                            mb_visited=True
                                        valid=False
                                elif Rkey==-1:
                                    if indexj>0:
                                        if i<2 and not key:
                                            if not mb_visited:
                                                messagebox.showinfo("안내","필수 키가 빠진 행은 추가되지 않습니다")
                                                mb_visited=True
                                            valid=False
                                    else:
                                        if i==0 and not key:
                                            if not mb_visited:
                                                messagebox.showinfo("안내","필수 키가 빠진 행은 추가되지 않습니다")
                                                mb_visited=True
                                            valid=False
                                elif i==Rkey:
                                    if not key:
                                        if not mb_visited:
                                            messagebox.showinfo("안내","필수 키가 빠진 행은 추가되지 않습니다")
                                            mb_visited=True
                                        valid=False

                                find=False
                                for k,v in Integration.items():
                                    if k==key:
                                        value[i]=v
                                        find=True
                                if not find:
                                    value[i]=key
                            indexj+=1
                            if valid:
                                new_items["".join(value)]=dial
            return new_items

        def on_append_button():
            data=load_content_json(project_dir)
            uniqueid=load_unique_id(data)
            if isromance():
                current=tab.pop()
                new_items=generate_dialogue_items(current)
                append_to_dialogue(new_items,True)
                new_items={k:v for k,v in new_items.items() if k.endswith(uniqueid) and not (k.startswith("funLeave") or k.startswith("jobLeave") or k.startswith("patio"))}
                append_to_dialogue(new_items,True,True)

                content={"Action": "Load","Target": f"Characters/Dialogue/MarriageDialogue{uniqueid}","FromFile": f"dialogue/MarriageDialogue{uniqueid}.json"}
                index=is_existing_data(content,data)
                if not index:
                    append_to_content(content,data)
                content={"Action": "EditData","Target": "Characters/Dialogue/MarriageDialogue","FromFile": "dialogue/MarriageDialogue.json"}
                index=is_existing_data(content,data)
                if not index:
                    append_to_content(content,data)
            current=tab.pop()
            append_to_dialogue(generate_dialogue_items(current,-1)) #대화주제/세계흐름
            for i in range(3):
                current=tab.pop()
                append_to_dialogue(generate_dialogue_items(current))
            current=tab.pop()
            append_to_dialogue(generate_dialogue_items(current,0)) #위치
            current=tab.pop()
            append_to_dialogue(generate_dialogue_items(current,1)) #일상
            content={"Action": "Load","Target": f"Characters/Dialogue/{uniqueid}","FromFile": f"dialogue/MarriageDialogue{uniqueid}.json"}
            index=is_existing_data(content,data)
            if not index:
                append_to_content(content,data)
            messagebox.showinfo("업로드 완료","대사를 성공적으로 업로드하였습니다")
            win.destroy()
            
        def add_tab(title):
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=title)
            # 캔버스 + 스크롤바 프레임
            canvas = tk.Canvas(tab)
            scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)

            # 내부 내용 담을 frame
            inner_frame = ttk.Frame(canvas)
            window_id = canvas.create_window((0, 0), window=inner_frame, anchor="n", tags="inner_frame")

            # 스크롤 영역 설정
            def on_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

                # inner_frame 너비를 캔버스에 맞추기
                canvas_width = canvas.winfo_width()
                canvas.itemconfig(window_id, width=canvas_width)

            # 캔버스 크기 변경 시에도 프레임 폭 맞추기
            def on_canvas_resize(event):
                canvas.itemconfig(window_id, width=event.width)

            inner_frame.bind("<Configure>", on_configure)
            canvas.bind("<Configure>", on_canvas_resize)

            append_btn=tk.Button(inner_frame,command=on_append_button,text="모두 저장하기");append_btn.pack(side="bottom",pady=10)
            return inner_frame

        current=add_tab("일상")
        tab.append(current)
        top_container=tk.Frame(current);top_container.pack(side="top")
        tk,Label(top_container,text="두 번째 콤보박스 제외 필수 XXX. 월~금 대사는 지정하는 것이 좋습니다").pack(side="top")
        def specific_rain():
            message=open_text_editor()
            if message:
                data=load_content_json(project_dir)
                characterID=load_unique_id(data)
                content={
                "Action": "EditData",
                "Target": "Characters/Dialogue/rainy",
                "Entries": {
                    characterID: message
                    }
                }
                append_to_content(content,data,is_existing_data(content,data))
            else: return
        tk.Button(top_container,text="또는 비 내리는 날 대사 지정하기",command=specific_rain).pack(side="top")
        create_dynamic_input(current,
                             values=[["","봄","여름","가을","겨울"],
                                     [k+"요일" for k in DayOfWeek.keys()]+[day+" 호감도"+str(num) for day in ["월","화","수","목","금","토","일"] for num in range(2,11,2)]+[str(num)+"일" for num in range(1,29)],
                                     ["",'1년차','그 이후'],
                                     [""]+[Name + "와 결혼" for Name in NPCName],open_text_editor],
                             side="top",btn_text=" 대사",res_width=40)

        current=add_tab("위치")
        tab.append(current)
        top_container=tk.Frame(current);top_container.pack(side="top")
        tk,Label(top_container,text="또는 특정 좌표의 대사 지정하기").pack(side="left")
        def specific_location():
            lc=select_location(mapname=None, numdirection=False, isdirection=False)
            if lc:
                message=open_text_editor()
            else: return
            if message:
                new_item={f"{lc[0]}_{lc[1]}_{lc[2]}":message}
            else: return
            append_to_dialogue(new_item)
        tk.Button(top_container,text="위치",command=specific_location).pack(side="left")
        create_dynamic_input(current,
                             values=[location_name,
                                     [""]+["월","화","수","목","금","토","일"]+
                                     [str(num)+"하트" for num in range(2,11,2)],open_text_editor],
                             side="top",btn_text=" 대사",res_width=40)

        current=add_tab("축제")
        tab.append(current)
        tk.Label(current,text="축제 일반").pack(side="top")
        create_dynamic_input(current,values=[list(festival_key.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)
        tk.Label(current,text="특정 아이템 반응").pack(side="top")
        create_dynamic_input(current,values=[["겨울별축제 선물반응"],list(sd_items.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)

        current=add_tab("아이템")
        tab.append(current)
        tk.Label(current,text="아이템 일반").pack(side="top")
        create_dynamic_input(current,values=[list(item_d_key.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)
        tk.Label(current,text="특정 아이템 거부 및 받기").pack(side="top")
        create_dynamic_input(current,values=[['생일선물받기','선물받기','특정선물거부'],list(sd_items.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)
        tk.Label(current,text="선호도에 따른 특정 아이템 받기").pack(side="top")
        create_dynamic_input(current,values=[['생일선물받기','선물받기'],list(taste.keys()),["-"]+[k for k,v in sd_items.items() if v.id<0],open_text_editor],side="top",btn_text=" 대사",res_width=40)

        current=add_tab("특별")
        tab.append(current)
        tk.Label(current,text="특정 상황에 대한 대사").pack(side="top")
        create_dynamic_input(current,values=[list(unique_key.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)
        tk.Label(current,text="특정 위치에 들어갈 때 이름 위에 50%로 출력되는 대사. \"/\"로 구분하여 랜덤으로 출력되도록 할 수 있습니다").pack(side="top")
        create_dynamic_input(current,values=[[name+"_Entry" for name in location_name],open_text_editor],side="top",btn_text=" 대사",res_width=40)
        
        current=add_tab("세계흐름")
        tab.append(current)
        tk.Label(current,text="특정 대화주제가 활성화 될 때 출력되는 대사입니다. 사용자가 직접 생성한 대화주제는 영문 그대로 입력해주세요\n또, 그것이 지속되는 기간을 확인하여 (X days) 날짜가 지남에 따라 대사를 다르게 지정할 수 있습니다").pack(side="top")
        create_dynamic_input(current,values=[list(event_dial_key.keys()),list(TheDayAfter.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)
        tk.Label(current,text="밑의 대화주제들은 모두 기간이 4일입니다.").pack(side="top")
        tk.Label(current,text="특정 NPC").pack(side="top")
        create_dynamic_input(current,values=[list(event_withNPC.keys()),NPCName,"(이)랑",list(TheDayAfter.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)
        tk.Label(current,text="농사 / 낚시").pack(side="top")
        create_dynamic_input(current,values=[list(event_withObj.keys()),[k+"을(를)" for k,v in sd_items.items() if v.id>0],"잡기/수확",list(TheDayAfter.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)
        tk.Label(current,text="이벤트").pack(side="top")
        create_dynamic_input(current,values=[["처음으로 이벤트"],list(event_info.keys()),"를 봄",list(TheDayAfter.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)
        tk.Label(current,text="장소").pack(side="top")
        create_dynamic_input(current,values=[["처음으로 장소"],location_name,"에 들어간다",list(TheDayAfter.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)
        tk.Label(current,text="업적/퀘스트 : 콤보박스 안에 값 입력").pack(side="top")
        create_dynamic_input(current,values=[["처음으로 업적 (id: ","처음으로 퀘스트 (id: "],[],") 를 완료",list(TheDayAfter.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)

        if isromance():
            current=add_tab("결혼")
            tab.append(current)
            tk.Label(current,text="결혼 일반").pack(side="top")
            create_dynamic_input(current,values=[list(marriged_key.keys()),open_text_editor],side="top",btn_text=" 대사",res_width=40)
            create_dynamic_input(current,values=[list(Season.keys()),[str(num)+"일" for num in range(1,29)],open_text_editor],side="top",btn_text=" 대사",res_width=40)
            tk.Label(current,text="하루가 시작될 때 매일 추가되는 무작위 대사입니다.\n각각 할당된 개수가 있어 그것을 다 채우지 못하면 게임의 기본 대사가 출력될 수 있습니다").pack(side="top")
            create_dynamic_input(current,values=["각각 5개",["비 오는 날","비 안 오는 날 또는 실내"],[str(num)+"번 대사" for num in range(1,6)],open_text_editor],side="top",btn_text=" 대사",res_width=40)
            create_dynamic_input(current,values=["7개",["비 내리는 저녁 농가"],[str(num)+"번 대사" for num in range(7)],open_text_editor],side="top",btn_text=" 대사",res_width=40)
            create_dynamic_input(current,values=["6개",["비 안 오는 저녁 농가"],[str(num)+"번 대사" for num in range(6)],open_text_editor],side="top",btn_text=" 대사",res_width=40)
            tk.Label(current,text="이 밑으로는 할당된 개수를 채우지 않아도 좋지만, 그것을 넘어서는 안 됩니다.").pack(side="top")
            create_dynamic_input(current,values=["각각 5개",["농장에서 80%로","부엌에서(자녀 한 명인 경우)","부엌에서(자녀 두 명인 경우)"],[str(num)+"번 대사" for num in range(1,6)],open_text_editor],side="top",btn_text=" 대사",res_width=40)
            tk.Label(current,text="애정 확률 - 하트 9미만: 나쁨/중립, 하트10개: 50%로 좋음, 하트11개:87.5%로 좋음, 하트 12개이상:99.4%로 좋음. 그 이외는 중립.").pack(side="top")
            create_dynamic_input(current,values=["각각 10개",["애정:나쁨","애정:중립","애정:좋음"],[str(num)+"번 대사" for num in range(1,11)],open_text_editor],side="top",btn_text=" 대사",res_width=40)
    def open_elsedialogue_editor():
        win = tk.Toplevel(root)
        win.title("특수 다이얼로그 편집기")
        win.geometry("700x400")
        notebook = ttk.Notebook(win)
        notebook.pack(expand=True, fill='both')
        tab=[]
        def add_tab(title):
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=title)
            # 캔버스 + 스크롤바 프레임
            canvas = tk.Canvas(tab)
            scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)

            # 내부 내용 담을 frame
            inner_frame = ttk.Frame(canvas)
            window_id = canvas.create_window((0, 0), window=inner_frame, anchor="n", tags="inner_frame")

            # 스크롤 영역 설정
            def on_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

                # inner_frame 너비를 캔버스에 맞추기
                canvas_width = canvas.winfo_width()
                canvas.itemconfig(window_id, width=canvas_width)

            # 캔버스 크기 변경 시에도 프레임 폭 맞추기
            def on_canvas_resize(event):
                canvas.itemconfig(window_id, width=event.width)

            inner_frame.bind("<Configure>", on_configure)
            canvas.bind("<Configure>", on_canvas_resize)

            return inner_frame
        #___________________________________________________________
        current=add_tab("퀘스트")
        questID=str(random_number_generate(4))
        tab.append(current)
        idlabel=tk.Label(current,text=f"배정된 퀘스트ID : {questID}, 어딘가에 메모해 주세요");idlabel.pack(side="top")

        quest_0_4_data={"Basic":["수동으로 처리, 적절한 시기에 완료해야함","-1"],
                        "Crafting":["제작가능아이템 /h create_image_combo(win, row, tp='c')/ 제작","(BC)<0>"],
                        "Location":["c location_name/ 방문","<0>"],
                        "Building":["c Building/ 하나라도 건설","<0:Building>"],
                        "ItemDelivery":["c NPCName/에게 /c Object/을(를) /e/개 전달","<0> (O)<1:Object> <2>"],
                        "Monster":["공백을 언더바로 바꾼 영어 몬스터 이름/e/을(를) /e/마리 죽이고 /c NPCName/과 대화하기","<0> <1> <2>"],
                        "ItemHarvest":["c Object/를 /e/번 수확","(O)<0:Object> <1>"],
                        "LostItem":["b10 locationandxy()/에 있는/c Object/을(를) /c NPCName/에게 전달하자","<2> (O)<1:Object> <0>"],
                        "SecretLostItem":["c Object/을(를) /c NPCName/에게 전달하면 호감도 변화 /e","<1> (O)<0:Object> <2>"],
                        "Social":["마을의 모든 사람과 대화하기","null"]
                        }

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="퀘스트 유형 ").pack(side="left")
        zero=ttk.Combobox(row,values=list(quest_0_4_data.keys()),width=10,state="readonly");zero.pack(side="left")
        zero.current(0)

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="퀘스트 표시 제목 ").pack(side="left")
        one=tk.Entry(row,width=20);one.pack(side="left")

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="퀘스트 표시 내용/설명 ").pack(side="left")
        two=tk.Entry(row,width=30);two.pack(side="left")

        tk.Label(current,text="이 아래로는 선택 사항입니다").pack(side="top",pady=10)

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="퀘스트 짧은 지침").pack(side="left")
        three=tk.Entry(row,width=20);three.pack(side="left")

        four=tk.Frame(current);four.pack(side="top")
        create_input_box(four,quest_0_4_data[zero.get()][0],False,win)
        def zero_selected(event):
            selected=zero.get()
            if selected in quest_0_4_data:
                for widget in four.winfo_children():
                    widget.destroy()
                create_input_box(four,quest_0_4_data[zero.get()][0],False,win)
        zero.bind("<<ComboboxSelected>>",zero_selected)

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="완료시 로그에 추가될 퀘스트 ID(다음 퀘스트)").pack(side="left")
        five=tk.Entry(row,width=20);five.pack(side="left")

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="완료시 주어지는 금액").pack(side="left")
        six=tk.Entry(row,width=5);six.pack(side="left")

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="취소 가능 여부 ").pack(side="left")
        eight=ttk.Combobox(row,values=['false','true'],width=10,state="readonly");eight.pack(side="left")
        eight.current(0)

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="지정된 NPC가 있다면 완료대사 ").pack(side="left")
        qbox=tk.Entry(row, width=20, state="readonly");qbox.pack(side="left")
        def qadd_handler():
            qbox.config(state="normal")
            qbox.delete(0,tk.END)
            textd=qbox.get()
            if textd=="end" or textd=="":
                textd=open_text_editor()
            else: textd=open_text_editor(message=textd)
            qbox.insert(0,textd)
            qbox.config(state="readonly")
        qadd=tk.Button(row,text="입력",command=qadd_handler);qadd.pack(side="left")

        def add_quest():
            result=[zero.get(),one.get(),two.get(),three.get(),"",five.get(),six.get(),"-1",eight.get(),qbox.get()]
            if not result[5]:result[5]="-1"
            if not result[6]:result[6]="0"
            if not result[8]:result[8]="false"
            if not result[9]:result.pop()
            for i in range(3):
                if not result[i]:
                    messagebox.showerror("오류","필수 항목이 비워져 있습니다")
                    return
            user_input=[]
            for row in four.winfo_children():
                if isinstance(row,tk.Frame):
                    for widget in row.winfo_children():
                        if isinstance(widget,ttk.Combobox):
                            user_input.append(widget.get())
                        elif isinstance(widget,tk.Entry):
                            user_input.append(widget.get())
            result[4]=extract_between(quest_0_4_data[zero.get()][1],user_input)
            data=load_content_json(project_dir)
            content={
                "Action": "EditData",
                "Target": "Data/Quests",
                "Entries": {}
            }
            modify_to_index=is_existing_data(content,data)
            if modify_to_index:
                content=data["Changes"][modify_to_index]
            nonlocal questID
            content["Entries"][questID]="/".join(result)
            append_to_content(content,data,modify_to_index)
            messagebox.showinfo("업로드 완료","퀘스트 데이터가 생성되었습니다")
            questID=str(random_number_generate(4))
            idlabel.config(text=f"배정된 퀘스트ID : {questID}, 어딘가에 메모해 주세요")
        tk.Button(current,text="퀘스트 추가",command=add_quest).pack(side="top",pady=10)
        #___________________________________________________________

        mail_command={
                        "없음": [" ",""],
                        "물건 포함":["아이템 /c Object/ 첨부","%item id (O)<0:Object> %%"],
                        "트리거 문자열":["트리거 액션 /e30","%action <0> %%"],
                        "제작가능아이템 포함":["아이템 /h create_image_combo(win, row, tp='c')/ 포함","%item id (BC)<0> %%"],
                        "돈 첨부":["e/G","%item money <0> %%"],
                        "랜덤 돈 첨부":["e/G ~ /e/G","%item money <0> <1> %%"],
                        "대화주제 활성화":["e/일 길이의 대화주제 /e20/활성화","%item conversationTopic <1> <0> %%"],
                        "요리 레시피 포함":["레시피 /c CookingRecepies/ 포함","%item cookingRecipe replace_blank('<0:CookingRecepies>') %%"],
                        "제작 레시피 포함":["레시피 /c CraftingRecepies/ 포함","%item craftingRecipe replace_blank('<0:CraftingRecepies>') %%"],
                        "말론이 찾은 물건 첨부":["Marlon이 광산에서 찾은 아이템 첨부","%item itemRecovery %%"],
                        "퀘스트 수락or거절":["퀘스트ID: /e10","%item quest <0> %%"],
                        "퀘스트 자동 추가":["퀘스트ID: /e10","%item quest <0> true %%"],
                        "특별주문 추가":["orderID:/e/, 자동수락여부: /c ['true','false']","%item specialOrder <0> <1> %%"]
                        }
        
        current=add_tab("메일")
        tab.append(current)

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="<letter ID> 지정").pack(side="left")
        keyE=tk.Entry(row,width=15);keyE.pack(side="left")
        tk.Label(current,text="계절_날짜, 계절_날짜_년도(1~2) 조합으로 지정하면\n해당 날짜에 메일이 도착합니다.\n(ex. spring_2_1, spring_12 , summer_2_2)\n또는 임의의 영문숫자언더바(공백없음) 조합의 ID를 지정할 시\n이벤트를 통해 트리거해야 합니다").pack(side="top")

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="짧은 메일 제목").pack(side="left")
        titleE=tk.Entry(row,width=20);titleE.pack(side="left")
        tk.Label(current,text="메일 내용").pack(side="top")
        detailE=tk.Text(current,width=40,height=20);detailE.pack(side="top")
        tk.Label(current,text=" 엔터나 ^ 는 문단 구분자, @ 는 플레이어 이름, ¦ 는 성별 구분자로\n앞의 텍스트는 남자, 뒤의 텍스트는 그 외의 플레이어에게 표시됩니다\n 문단 구분자를 통해 받는 사람과 주는 사람, 추신 등을 표현하세요\n%secretsanta: 겨울 18~25에는 랜덤 NPC이름, 아니면 ???로 대체").pack(side="top")
        

        row=tk.Frame(current);row.pack(side="top")
        tk.Label(row,text="특수 명령 추가하기").pack(side="left",pady=10)
        ctcb=ttk.Combobox(row,values=list(mail_command.keys()),width=20,state="readonly");ctcb.pack(side="left")
        ctcb.current(0)

        mail_cmd_ct=tk.Frame(current);mail_cmd_ct.pack(side="top")
        create_input_box(mail_cmd_ct,mail_command[ctcb.get()][0],False,win)
        def ctcb_selected(event):
            selected=ctcb.get()
            if selected in mail_command:
                for widget in mail_cmd_ct.winfo_children():
                    widget.destroy()
                create_input_box(mail_cmd_ct,mail_command[ctcb.get()][0],False,win)
        ctcb.bind("<<ComboboxSelected>>",ctcb_selected)

        def add_mail():
            key=keyE.get().strip()
            title=titleE.get()
            detail=detailE.get("1.0","end-1c")
            detail=detail.replace("\n","^")

            user_input=[]
            for row in mail_cmd_ct.winfo_children():
                if isinstance(row,tk.Frame):
                    for widget in row.winfo_children():
                        if isinstance(widget,ttk.Combobox):
                            user_input.append(widget.get())
                        elif isinstance(widget,tk.Entry):
                            user_input.append(widget.get())
            try:
                mail_cmd=" ".join(parse_input_string_tokens(mail_command[ctcb.get()][1],user_input))
            except:
                mail_cmd=""
            data=load_content_json(project_dir)
            content={
                "Action": "EditData",
                "Target": "Data/mail",
                "Entries": {}
            }
            modify_to_index=is_existing_data(content,data)
            if modify_to_index:
                content=data["Changes"][modify_to_index]
            content["Entries"][key]=detail+mail_cmd
            if title:
                content["Entries"][key]+="[#]"+title
            append_to_content(content,data,modify_to_index)
            messagebox.showinfo("업로드 완료","메일 데이터가 생성되었습니다")
        tk.Button(current,text="메일 추가",command=add_mail).pack(side="top",pady=10)

        #___________________________________________________________

        current=add_tab("기타")
        tab.append(current)
        tk.Label(current, text="준비 중인 기능입니다...\n룸메 대화/축제 대화/쓰레기통/영화관 대화 등등").pack(padx=20, pady=20)
    def open_schedule_editor():
        ScheduleKey={
                     "계절기반":["c Season/c DayKey","<0:Season><1:DayKey>"],
                     "날짜기반":["날짜:/e/일,/c HeartKey","<0><1:HeartKey>"],
                     "축제":["c MarriageKey/ 축제/c ['NightMarket','DesertFestival','TroutDerby','SquidFest']/c FestivalDay","<0:MarriageKey><1><2:FestivalDay>"],
                     "요일기반":["c SeasonKey/c DayOfWeek/c HeartKey","<0:SeasonKey><1:DayOfWeek><2:HeartKey>"],
                     "비오는날":["비 오는 날에 적용됩니다","rain"],
                     "비오는날2(확률50%)":["비 오는 날에 적용될 확률은 50%입니다","rain2"],
                     "결혼+날짜":["결혼 후 /c Season/e/일","marriage_<0:Season>_<1>"],
                     "결혼+비X요일":["결혼 후 /c DayOfWeek","marriage_<0:DayOfWeek>"]
                     }
        def extract_date_key(item):
            s = item[1].split()[0]  # "a630", "1230", etc. — 첫 단어
            digits = ''.join(filter(str.isdigit, s))  # 숫자만 추출
            return int(digits)

        class ScheduleEditor(tk.Tk):
            def __init__(self):
                super().__init__()
                self.title("스케줄 생성")
                self.geometry("1000x600")
                
                self.hours = self.generate_hours()
                self.days = {"봄":["spring","",[]]} #스케쥴의 요일 항목 korkey:[internal key, val(goto 등 조건문),[블록이름1,시간~장소대사][블록이름2,]]
                self.cols= {}

                # 전체 프레임 구성
                self.left_frame = tk.Frame(self, width=200, bg="lightgrey")
                self.left_frame.pack(side="left", fill="y")
        
                self.right_frame = tk.Frame(self)
                self.right_frame.pack(side="right", fill="both", expand=True)
        
                self.create_left_panel()
                self.create_right_panel()   
            def create_left_panel(self):
                # 블록 추가/제거 영역
                tk.Label(self.left_frame, text="경로 목록", bg="lightgrey").pack(pady=10)
                
                self.block_to_command={}

                self.block_listbox = tk.Listbox(self.left_frame, height=10)
                self.block_listbox.pack(pady=5, padx=10, fill="x")
                if isromance():
                    self.block_listbox.insert("end", "(결혼한 경우) 자러 간다")
                    self.block_to_command["(결혼한 경우) 자러 간다"]=[" bed","#505050"]
        
                button_frame = tk.Frame(self.left_frame, bg="lightgrey")
                button_frame.pack(pady=10)
        
                tk.Button(button_frame, text="경로+", width=5, command=self.add_block).pack(side="left", padx=5)
                tk.Button(button_frame, text="경로-", width=5, command=self.remove_block).pack(side="left", padx=5)
        
                tk.Button(self.left_frame, text="경로 시간표에 삽입", command=self.place_block).pack(pady=10)
                def on_listbox_double_click(event):
                    self.place_block()
                self.block_listbox.bind("<Double-Button-1>",on_listbox_double_click)

                tk.Button(self.left_frame,text="조건 추가",command=self.add_condition).pack(pady=10)
                tk.Label(self.left_frame,text="Tip.\n봄 또는 봄+요일은 예외가\n발생했을 때 디폴트 값으로\n쓰입니다.").pack(pady=5)
                tk.Button(self.left_frame,text="모두 저장하고 닫기",command=self.save_handler).pack(pady=10)
                
            def create_right_panel(self):
                # 캔버스 및 스크롤바 포함한 시간표
                canvas_frame = tk.Frame(self.right_frame)
                canvas_frame.pack(fill="both", expand=True)
        
                self.canvas = tk.Canvas(canvas_frame, bg="white")
                self.hbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
                self.vbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
                self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
                
                self.hbar.pack(side="bottom", fill="x")
                self.vbar.pack(side="right", fill="y")
                self.canvas.pack(side="left", fill="both", expand=True)
                # 내부 프레임
                self.inner_frame = tk.Frame(self.canvas)
                self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

                def on_configure(event):
                    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

                self.inner_frame.bind("<Configure>", on_configure)

                # 시간열 먼저 추가
                time_column = tk.Frame(self.inner_frame)
                time_column.pack(side="left", fill="y")
                blank = tk.Label(time_column, text="", width=10, height=1)
                blank.pack(side="top")
                for hour in self.hours:
                    tk.Label(
                        time_column,
                        text=f"{hour[:2]}:{hour[2:]}",
                        width=10,
                        height=1,
                        bg="white" if hour[2:] == "30" else "#f0f0f0",
                    ).pack(side="top")
                
                for k,v in self.days.items():
                    self.add_row(k)
            def add_condition(self):
                win = tk.Toplevel(self)
                win.title("열 추가")
                win.geometry("600x400")
                ctcb=ttk.Combobox(win,values=list(ScheduleKey.keys()),state="readonly",width=15);ctcb.pack(side="top",pady=20)
                ctcb.current(0)
                def on_add_btn():
                    category=ctcb.get()
                    win2=tk.Toplevel(win)
                    win2.title("제목 입력")
                    title=""
                    tk.Label(win2,text="제목 지정").pack(side="top")
                    titleE=tk.Entry(win2,width=15);titleE.pack(side="top")
                    titleE.insert(0,category)
                    def on_OK_btn():
                        nonlocal title
                        title=titleE.get()
                        if not title:
                            messagebox.showerror("오류","공백은 불가합니다")
                            return
                        elif title in self.days.keys():
                            messagebox.showerror("오류","동일한 제목의 일정이 이미 존재합니다")
                            return
                        win2.destroy()
                    tk.Button(win2,text="완료",command=on_OK_btn).pack(side="bottom",pady=10)
                    win2.wait_window()
                    if not title:
                        return
                    user_input=[]
                    for widget in win.winfo_children():
                        if widget!=bottom_container:
                            if isinstance(widget,tk.Frame):
                                for wdg in widget.winfo_children():
                                    if isinstance(wdg,ttk.Combobox):
                                        if wdg not in user_input:
                                            user_input.append(wdg)
                                    if isinstance(wdg,tk.Entry):
                                        if wdg not in user_input:
                                            user_input.append(wdg)
                    for i in range(len(user_input)):
                        user_input[i]=user_input[i].get()
                    cmd2=[]
                    if select==0:
                        initial_cmd=""
                    elif select==1:
                        initial_cmd=alternfirstKey[point[0].get()]
                        cmd2=None
                    elif select==2:
                        initial_cmd="NOT friendship"
                        point.clear()
                        for i, fr in enumerate(frame):
                            if i == 2:
                                for widget in fr.winfo_children():
                                    if isinstance(widget,ttk.Combobox):
                                        if widget not in point:
                                            point.append(widget)
                                    if isinstance(widget,tk.Entry):
                                        if widget not in point:
                                            point.append(widget)
                                    if isinstance(widget,tk.Frame):
                                        for wdg in widget.winfo_children():
                                            if isinstance(wdg,tk.Frame):
                                                for wg in wdg.winfo_children():
                                                    if isinstance(wg,ttk.Combobox):
                                                        if wg not in point:
                                                            point.append(wg)
                        for i in range (0,len(point)-1,2):
                            initial_cmd+=f" {point[i].get()} {point[i+1].get()}"
                        initial_cmd+=initialKey[point[-1].get()]
                    elif select==3:
                        letterID=point[0].get()
                        initial_cmd=f"MAIL {letterID}"+initialKey[point[1].get()]

                    self.days[title]=[extract_between(ScheduleKey[category][1],user_input),initial_cmd,cmd2]
                    self.add_row(title)
                    win.destroy()
                add_btn=tk.Button(win,text="추가",command=on_add_btn);add_btn.pack(side="bottom",pady=10)
                bottom_container=tk.Frame(win);bottom_container.pack(side="bottom")
                def on_select(event):
                    for widget in win.winfo_children():
                        if widget!=ctcb and widget!=add_btn and widget!=bottom_container:
                            widget.destroy()
                    category=ctcb.get()
                    create_input_box(win,ScheduleKey[category][0])
                ctcb.bind("<<ComboboxSelected>>",on_select)

                #bottom_container
                tk.Label(bottom_container,text="\"선택안함\"이 있는 항목은 필수가 아닙니다.").pack(side="top",pady=20)
                alternfirstKey={f"{k}":f"GOTO {v[0]}" for k,v in self.days.items()}
                alternativeKey={f"{k}(으)로 대체":f"/GOTO {v[0]}" for k,v in self.days.items()}
                initialKey={"종료":""}|alternativeKey

                def update_state(selected_index):
                    # 체크 상태 갱신
                    for i in range(4):
                        if i == selected_index:
                            check_vars[i].set(True)
                            cbbtn[i].select()
                            nonlocal select
                            select=i
                            point.clear()
                        else:
                            check_vars[i].set(False)
                            cbbtn[i].deselect()
                    # 위젯 상태 갱신
                    for i, fr in enumerate(frame):
                        if i == selected_index:
                            for widget in fr.winfo_children():
                                if isinstance(widget,ttk.Combobox):
                                    if widget not in point:
                                        widget.config(state="readonly")
                                        point.append(widget)
                                if isinstance(widget,tk.Entry):
                                    if widget not in point:
                                        widget.config(state="normal")
                                        point.append(widget)
                                if isinstance(widget,tk.Frame):
                                    for wdg in widget.winfo_children():
                                        if isinstance(wdg,tk.Frame):
                                            for wg in wdg.winfo_children():
                                                if isinstance(wg,ttk.Combobox):
                                                    if wg not in point:
                                                        wg.config(state="normal")
                                                        point.append(wg)
                                                if isinstance(wg,tk.Button):
                                                    wg.config(state="normal")
                        else:
                            for widget in fr.winfo_children():
                                if isinstance(widget,ttk.Combobox):
                                    widget.config(state="disabled")
                                if isinstance(widget,tk.Entry):
                                    widget.config(state="disabled")
                                if isinstance(widget,tk.Frame):
                                    for wdg in widget.winfo_children():
                                        if isinstance(wdg,tk.Frame):
                                            for wg in wdg.winfo_children():
                                                if isinstance(wg,ttk.Combobox):
                                                    wg.config(state="disabled")
                                                if isinstance(wg,tk.Button):
                                                    wg.config(state="disabled")
                
                check_vars = [tk.BooleanVar(value=0) for _ in range(4)]
                frame=[]
                cbbtn=[]
                select=0
                point=[]
                # ① 대체코드 미사용 (Label only)
                frame1 = tk.Frame(bottom_container)
                frame1.pack(anchor="w")
                cb1 = tk.Checkbutton(frame1, variable=check_vars[0], command=lambda: update_state(0))
                cb1.pack(side="left")
                cbbtn.append(cb1);cb1.select()
                tk.Label(frame1, text="대체코드 미사용").pack(side="left")
                frame.append(frame1)

                # ② 
                frame2 = tk.Frame(bottom_container)
                frame2.pack(anchor="w")
                cb2 = tk.Checkbutton(frame2, variable=check_vars[1], command=lambda: update_state(1))
                cb2.pack(side="left")
                cbbtn.append(cb2)
                ttk.Combobox(frame2,values=list(alternfirstKey.keys()),state='disabled').pack(side="left")
                tk.Label(frame2, text="(으)로 대체").pack(side="left")
                frame.append(frame2)

                # ② NPC 호감도 입력칸
                frame3 = tk.Frame(bottom_container)
                frame3.pack(anchor="w")
                cb3 = tk.Checkbutton(frame3, variable=check_vars[2], command=lambda: update_state(2))
                cb3.pack(side="left")
                cbbtn.append(cb3)
                create_dynamic_input(frame3,[NPCName,' 하트',[str(num) for num in range(2,11,2)],'이상'],side="left")
                tk.Label(frame3,text="이면 ").pack(side="left")
                lastcb=ttk.Combobox(frame3,values=list(initialKey.keys()),state='disabled');lastcb.pack(side="left")
                lastcb.current(0)
                for widget in frame3.winfo_children():
                    if isinstance(widget,tk.Frame):
                        for wdg in widget.winfo_children():
                            if isinstance(wdg,tk.Frame):
                                for wg in wdg.winfo_children():
                                    if isinstance(wg,ttk.Combobox):
                                        wg.config(state="disabled")
                                    if isinstance(wg,tk.Button):
                                        wg.config(state="disabled")
                frame.append(frame3)
                
                # ③ Letter ID (Combobox)
                frame4 = tk.Frame(bottom_container)
                frame4.pack(anchor="w")
                cb4 = tk.Checkbutton(frame4, variable=check_vars[3], command=lambda: update_state(3))
                cb4.pack(side="left")
                cbbtn.append(cb4)
                tk.Label(frame4, text="LetterID/세계상태ID").pack(side="left")
                tk.Entry(frame4, width=10, state='disabled').pack(side="left")
                tk.Label(frame4,text="(이)가 활성화 상태라면 ").pack(side="left")
                ttk.Combobox(frame4,values=list(initialKey.keys()),state='disabled').pack(side="left")
                frame.append(frame4)
            def generate_hours(self):
                # 시간 문자열 리스트 만들기
                hours = [f"0{h}00" for h in range(6, 10)] + [f"0{h}30" for h in range(6, 10)]
                hours += [f"{h}00" for h in range(10, 25)] + [f"{h}30" for h in range(10, 24)]
                return sorted(hours)
            def add_row(self, day):
                    if self.cols.get(day):
                        self.cols[day].destroy()
                    row_frame = tk.Frame(self.inner_frame)
                    row_frame.pack(side="left", fill="y", padx=5)
                    
                    top_container=tk.Frame(row_frame);top_container.pack(side="top")
                    tk.Label(top_container, text=day, width=10, height=1, bg="lightblue", relief="solid", bd=1).pack(side="left")
                    tk.Button(top_container,text="-",command=lambda: self.remove_row(day)).pack(side="left")

                    tmp_txt="";lb_txt="";tmp_color="white"
                    for hour in self.hours:
                        if self.days[day][2]==None:
                            tk.Label(
                            row_frame,
                            width=10,
                            height=1,
                            bg="grey"
                            ).pack(side="top")
                        else:
                            for cmd in self.days[day][2]:
                                st = cmd[1].split()[0]  # "a630", "1230", etc. — 첫 단어
                                digits = ''.join(filter(str.isdigit, st))  # 숫자만 추출
                                if int(hour)<=int(digits)<int(hour)+30:
                                    tmp_txt=cmd[0]
                                    tmp_color=self.block_to_command[cmd[0]][1]
                                    break;
                            if len(tmp_txt)>10:
                                try:
                                    lb_txt=tmp_txt[:10]
                                    tmp_txt=tmp_txt[10:]
                                except:
                                    lb_txt=tmp_txt
                                    tmp_txt=""
                            else:
                                lb_txt=tmp_txt
                                tmp_txt=""
                            if not lb_txt:
                                if hour[2:] == "30":
                                    tmp_color="white"
                                else:tmp_color="#f0f0f0"
                            tk.Label(
                                row_frame,
                                width=10,
                                height=1,
                                text=lb_txt,
                                bg=tmp_color
                                ).pack(side="top")

                    self.cols[day] = row_frame        
            def add_block(self):
                location=select_location(None,numdirection=True) #(맵이름,x,y,숫자방향)
                if not location:
                    return
                win = tk.Toplevel(self)
                win.title("일정 제목")
                win.geometry("300x100")
                lc_container=tk.Frame(win);lc_container.pack(side="top")
                
                name=tk.Entry(lc_container,width=30)
                name.insert(0,f"{location[0]}의 x:{location[1]},y:{location[2]},dir:{location[3]}으로 이동")
                name.pack(side="left",pady=10)
                def btn_handler():
                    title=name.get()
                    if not title:
                        messagebox.showerror("오류","공백은 불가합니다")
                        return
                    elif title in self.block_to_command:
                        messagebox.showerror("오류","같은 이름의 일정이 이미 존재합니다")
                        return
                    self.block_listbox.insert("end", title)
                    self.block_to_command[title]=[f" {location[0]} {location[1]} {location[2]} {location[3]}",generate_pastel_color()]
                    win.destroy()
                tk.Button(win,text="추가",command=btn_handler).pack(side="top",pady=10)
            def remove_block(self):
                selected = self.block_listbox.curselection()
                if selected:
                    block_name = self.block_listbox.get(selected[0])  # 삭제 전 이름 저장
                    self.block_listbox.delete(selected[0])
                    # block_to_command에서 삭제
                    if block_name in self.block_to_command:
                        del self.block_to_command[block_name]
                    # place_block 전부 삭제
                    for k, v in self.days.items():
                        new_items = [item for item in v[2] if item[0] != block_name]
                        if len(new_items) != len(v[2]):
                            self.days[k][2] = new_items
                            self.add_row(k)
            def remove_row(self,day):
                del self.days[day]
                self.cols[day].destroy()
                del self.cols[day]
            def place_block(self):
                selected = self.block_listbox.get("anchor")
                if not selected:
                    return
                win = tk.Toplevel(self)
                win.title(f"{selected} 일정 추가")
                win.geometry("400x200")
                
                top_container=tk.Frame(win);top_container.pack(side="top",pady=10)
                tk.Label(top_container,text="키 지정").pack(side="left")
                day_cb=ttk.Combobox(top_container,values=list(self.days.keys()),state="readonly",width=10);day_cb.pack(side="top")
                day_cb.current(0)

                #첫번째스크립트
                time_container=tk.Frame(win);time_container.pack(side="top")
                hour_cb=ttk.Combobox(time_container,values=list(range(6,25)),width=5);hour_cb.pack(side="left")
                hour_cb.current(0)
                tk.Label(time_container,text=":").pack(side="left")
                min_cb=ttk.Combobox(time_container,values=["00","30"],width=5);min_cb.pack(side="left")
                min_cb.current(0)
                is_timeA={"에 출발":"","까지 도착":"a"}
                is_timeA_cb=ttk.Combobox(time_container,values=list(is_timeA.keys()),width=5);is_timeA_cb.pack(side="left")
                is_timeA_cb.current(0)

                #애니메이션
                anim_container=tk.Frame(win);anim_container.pack(side="top")
                tk.Label(anim_container,text="(필수X) 도착하고 ").pack(side="left")
                animaE=tk.Entry(anim_container,width=10,state="readonly");animaE.pack(side="left")
                def anim_handler():
                    animkey=animation_manager(True)
                    if animkey:
                        animaE.config(state="normal")
                        animaE.delete(0,tk.END)
                        animaE.insert(0,animkey)
                        animaE.config(state="readonly")
                tk.Button(anim_container,text="애니추가",command=anim_handler).pack(side="left")
                
                #대사 키 미리 지정
                data=load_content_json(project_dir)
                content={
                        "Action": "Load",
                        "Target": f"Strings/schedules/{characterID}",
                        "Entries": {}
                        }
                modifytoindex=is_existing_data(content,data)
                if modifytoindex:
                    content=data["Changes"][modifytoindex]
                daykey=self.days[day_cb.get()][0]
                number=0
                dialkey=daykey+"."+str(number).zfill(3)
                while dialkey in content["Entries"]:
                    number+=1
                    dialkey=daykey+"."+str(number).zfill(3)
                #대사 키 입력받기
                tk.Label(win,text="대사는 선택사항이므로 원하지 않는다면 공백으로 두세요").pack(side="top")
                dial_container=tk.Frame(win);dial_container.pack(side="top")
                dialE=tk.Entry(dial_container,width=10,state="readonly");dialE.pack(side="left")
                def dial_handler():
                    text=open_text_editor()
                    if text: 
                        content["Entries"][dialkey]=text
                        dialE.config(state="normal")
                        dialE.delete(0,tk.END)
                        dialE.insert(0,text)
                        dialE.config(state="readonly")
                tk.Button(dial_container,text="대사추가",command=dial_handler).pack(side="left")

                def on_complete_place():
                    result=""
                    result+=is_timeA[is_timeA_cb.get()]
                    hour=int(hour_cb.get());minu=int(min_cb.get())
                    if hour<=6:
                        if minu<10:
                            minu=10
                    hour=str(hour);minu=str(minu).zfill(2)
                    result+=f"{hour}{minu}"
                    result+=self.block_to_command[selected][0]
                    animK=animaE.get()
                    if animK:
                        result+=f" {animK}"
                    dialK=dialE.get()
                    try:
                        if dialK:
                            result+=f" \"Strings\\schedules\\{characterID}:{dialkey}\""
                            append_to_content(content,data,modifytoindex)
                        self.days[day_cb.get()][2].append([selected,result])
                        #시간순으로 정렬
                        self.days[day_cb.get()][2] = sorted(self.days[day_cb.get()][2], key=extract_date_key)
                        self.add_row(day_cb.get())
                    except:
                        messagebox.showerror("오류","대체 키를 지정한 항목에는 일정을 삽입할 수 없습니다")
                    win.destroy()
                tk.Button(win,text="완료",command=on_complete_place).pack(side="top",pady=10)
            def save_handler(self):
                result={}
                for item in self.days.values():
                    command=""
                    if item[0]:
                        if item[1]:
                            command+=item[1]
                            if item[2]:
                                command+="/"+"/".join([token[1] for token in item[2]])
                        else: #GOTO 등의 조건문이 없다면
                            command+="/".join([token[1] for token in item[2]])
                        result[item[0]]=command
                append_to_schedule(result)
                content={
                    "Action": "Load",
                    "Target": f"Characters/schedules/{characterID}",
                    "FromFile": f"schedules/{characterID}.json",
                    }
                if not is_existing_data(content):
                    append_to_content(content)
                self.destroy()
        ScheduleEditor()

    def npc_option_editor():
        win = tk.Toplevel(root)
        win.title("기타 옵션 수정하기")
        tk.Label(win, text="준비 중인 기능입니다...\nhttps://stardewvalleywiki.com/Modding:NPC_data을 참고하세요").pack(padx=20, pady=20)
    def open_event_manager():
        class LocationListManager:
            def __init__(self, root):
                self.root = root
                self.event_info=load_event_info()
                self.eventdata = {}   # {location: [ (name, eid), ... ]}
                for lc, nm, eid in self.event_info:
                    if lc in self.eventdata:
                        self.eventdata[lc].append((nm,eid))
                    else:
                        self.eventdata[lc]=[(nm,eid)]
                
                self.ui = {}    # {location: (label1, listbox1, )}
        
                self.container = tk.Frame(root)
                self.container.pack(padx=10, pady=10, fill='both', expand=True)
        
                self.no_data_label = tk.Label(self.container, text="데이터 없음", font=("Arial", 16))
                self.no_data_label.pack(pady=50)
        
                btn = tk.Button(root, text="항목 추가", command=self.add_entry)
                btn.pack(pady=10)

                if self.eventdata:
                    self.no_data_label.pack_forget()
                    for location in self.eventdata:
                        self.build_location_ui(location)
                        self.refresh_location_listboxes(location)
        
            def add_entry(self):
                self.root.destroy()
                open_event_editor()
            def build_location_ui(self, location):
                if self.no_data_label.winfo_ismapped():
                    self.no_data_label.pack_forget()
        
                label1 = tk.Label(self.container, text=f"{location} 이름들")
                label1.pack()
                listbox1 = tk.Listbox(self.container, height=3, exportselection=False)
                listbox1.pack()

                delete_btn = tk.Button(self.container, text=f"{location} 선택 항목 삭제", 
                                       command=lambda loc=location: self.delete_selected(loc))
                delete_btn.pack(pady=(0, 10))
        
                self.ui[location] = (label1, listbox1, delete_btn)
        
            def refresh_location_listboxes(self, location):
                label1, listbox1, _ = self.ui[location]
                listbox1.delete(0, tk.END)
        
                for name, eid in self.eventdata[location]:
                    listbox1.insert(tk.END, name)
        
            def delete_selected(self, location):
                _, listbox1,_ = self.ui[location]
                selected_idx = listbox1.curselection()
                if not selected_idx:
                    return
                index = selected_idx[0]
                eventname=self.eventdata[location][index][0]
                eid=self.eventdata[location][index][1]
                try:
                    del self.eventdata[location][index]
                    #content에 이벤트 저장
                    if location in location_name:
                        content={
                            "Action": "EditData",
                            "Target": f"Data/Events/{location}",
                            "Entries": {}
                        }
                    else:
                        content={
                            "Action": "Load",
                            "Target": f"Data/Events/{location}",
                            "Entries": {}
                        }
                    contentdata=load_content_json(project_dir)
                    modifytoindex=is_existing_data(content,contentdata)
                    if modifytoindex:
                        content=contentdata["Changes"][modifytoindex]
                        for k in list(content["Entries"].keys()):
                            if k.startswith(eid):
                                del content["Entries"][k]
                        append_to_content(content,contentdata,modifytoindex)

                    new_lines=""
                    for token in self.event_info:
                        if token[2]==eid:
                            self.event_info.remove((location,eventname,eid))
                    for lc, nm, eid in self.event_info:
                        new_lines+=f"{lc}/{nm}/{eid}\n"
                    characterID=load_unique_id(data)
                    with open(os.path.join("content", "user_data", "event_data", f"{characterID}.txt"), "w", encoding="utf-8") as f:
                        f.writelines(new_lines) #이벤트 관리 메모장에 업데이트

                except IndexError:
                    return
        
                if not self.eventdata[location]:
                    # 데이터 없으면 UI 제거
                    for widget in self.ui[location]:
                        widget.destroy()
                    del self.ui[location]
                    del self.eventdata[location]
        
                    if not self.eventdata:
                        self.no_data_label.pack(pady=50)
                else:
                    self.refresh_location_listboxes(location)
        
        win = tk.Toplevel(root)
        win.title("이벤트 매니저")
        LocationListManager(win)


    #_____________________UI___________
    advanced_frame = tk.Frame(root)
    advanced_frame.pack(padx=10, pady=10, fill="both", expand=True)
    # 메뉴명 → 핸들러, 아이콘 파일명
    data=load_content_json(project_dir)
    characterID=load_unique_id(data)
    MENU = [
        ("초상화 업로드", open_portrait_uploader),
        ("스프라이트 생성", choose_load_or_open_sprite),
        ("선물 선호도",    open_gift_preferences),
        ("다이얼로그 편집", open_dialogue_editor),
        ("스케줄",         open_schedule_editor),
        ("이벤트",         open_event_manager),
        ("NPC 옵션",       npc_option_editor),
        ("특수 다이얼로그", open_elsedialogue_editor)
        ]

    #버튼추가
    for i, (label, cmd) in enumerate(MENU):
        icon_path=os.path.join(os.getcwd(), "content", "icon", label+".png")
        if os.path.isfile(icon_path):
            img = Image.open(icon_path).resize((32,32), Image.LANCZOS)
            icons.append(ImageTk.PhotoImage(img))
        else:
            icons.append(None) # 없으면 텍스트 버튼으로 표시

        btn = tk.Button(advanced_frame,
            text="   "+label,
            image=icons[i],
            compound="left",
            width=150,
            anchor="w",
            command=cmd
        )
        btn.grid(row=i, column=0, padx=10, pady=5, sticky="w")

root.mainloop()
