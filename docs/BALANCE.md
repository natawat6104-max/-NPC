# ตารางตัวเลขกลาง (Balance)

> ไฟล์นี้สร้างอัตโนมัติจาก `data/balance.json` — ห้ามแก้ด้วยมือ
> แก้ตัวเลขที่ JSON แล้วรัน `python3 tools/gen_balance_doc.py`
> ค่าที่ระบุที่มาว่า "ใหม่ — ต้องทดสอบ" ไม่มีในเอกสาร GDD เดิม

## เวลาและการจำลอง

| คีย์ | ค่า | หน่วย | หมายเหตุ | ที่มา |
|---|---|---|---|---|
| `time.periods_per_day` | 4 | ช่วง/วัน | เช้า กลางวัน เย็น กลางคืน; 1 tick = 1 ช่วง | GDD เจาะลึก 4.2 |
| `time.days_per_season` | 28 | วัน | ใช้กับฤดูกาลและช่วงพักฟื้นหลังวิกฤต | ใหม่ — ต้องทดสอบ |
| `time.speed_normal_seconds_per_period` | 3.0 | วินาทีจริง/ช่วง | ความเร็วปกติ | ใหม่ — ต้องทดสอบ |
| `time.speed_fast_multiplier` | 4 | เท่า | ความเร็ว 'เร็ว' | ใหม่ — ต้องทดสอบ |
| `time.speed_very_fast_multiplier` | 12 | เท่า | ความเร็ว 'เร็วมาก' | ใหม่ — ต้องทดสอบ |
| `time.pause_on_important_event` | ใช่ |  | ค่าเริ่มต้น: หยุดเวลาเมื่อมีเหตุการณ์สำคัญ | GDD เจาะลึก 12.4 |

## อิทธิพลของกลุ่มดาว

| คีย์ | ค่า | หน่วย | หมายเหตุ | ที่มา |
|---|---|---|---|---|
| `influence.cap` | 100 | แต้ม | ส่วนเกินเพดานสูญไป | GDD เจาะลึก 9.2 / ภาคผนวกอิทธิพล 3.1 |
| `influence.start` | 60 | แต้ม | แต้มเริ่มแคมเปญ | ภาคผนวกอิทธิพล 3.1 |
| `influence.regen_per_day` | 10 | แต้ม/วันเกม | ฟื้นต่อเนื่องตามเวลาเกม (ไม่ใช่เวลาจริง) | GDD เจาะลึก 9.2 (DECISIONS D3) |
| `influence.story_bonus_enabled` | ไม่ |  | MVP ไม่มีโบนัสแต้มจากเหตุการณ์ ใช้การฟื้นพื้นฐานอย่างเดียว | ภาคผนวกอิทธิพล 3.4 |
| `influence.max_per_event` | 30 | แต้ม | แต้มที่ใส่ในเหตุการณ์เดียวได้สูงสุด | ภาคผนวกอิทธิพล 5.4 |
| `influence.diminishing_full_points` | 15 | แต้ม | แต้มแรกในเหตุการณ์นับเต็ม | ภาคผนวกอิทธิพล 6.2 |
| `influence.diminishing_half_points` | 15 | แต้ม | แต้มถัดไปนับครึ่ง | ภาคผนวกอิทธิพล 6.2 |
| `influence.support_to_chance_ratio` | 0.25 | จุด%/แต้มประสิทธิผล | แปลงแต้มสนับสนุนเป็นโอกาสสำเร็จ | ภาคผนวกอิทธิพล 6.4 |
| `influence.chance_bonus_cap` | 15 | จุด% | โบนัสโอกาสรวมสูงสุดต่อเหตุการณ์ | ภาคผนวกอิทธิพล 6.4 |
| `influence.damage_reduction_cap` | 20 | % | ลดความเสียหายรวมสูงสุดต่อเหตุการณ์ | ภาคผนวกอิทธิพล 6.5 |

## พลังกลุ่มดาว (คูลดาวน์แปลงจากภาคผนวก: 24 ชม.จริง = 1 วันเกม = 4 ช่วง)

| คีย์ | ค่า | หน่วย | หมายเหตุ | ที่มา |
|---|---|---|---|---|
| `powers.watch` | cost=0, cooldown_periods=0, mvp=ใช่ |  | จับตามอง NPC หลัก 1 คน เปลี่ยนได้อิสระในโหมดเล่นคนเดียว | ภาคผนวกอิทธิพล 8.1 (DECISIONS D3) |
| `powers.foresee` | cost=8, cooldown_periods=1, mvp=ใช่ |  | พยากรณ์: แสดงช่วงความเสี่ยงและความเชื่อมั่น | ภาคผนวกอิทธิพล 8.2 |
| `powers.omen` | cost=12, cooldown_periods=1, mvp=ใช่ |  | ส่งลาง: เปิดเผยเบาะแสที่มีอยู่ ไม่หักแต้มถ้าไม่มีลางให้ส่ง | ภาคผนวกอิทธิพล 8.3 |
| `powers.blessing` | cost=25, cooldown_periods=2, mvp=ใช่, chance_bonus_pp=6 |  | ประทานพร: +5–8 จุด% (ใช้ 6) ภายใต้เพดานรวม | ภาคผนวกอิทธิพล 8.4 |
| `powers.gift` | cost=30, cooldown_periods=4, mvp=ใช่ |  | ของขวัญจากฟ้า: ของพื้นฐาน 1 ชุด ขายต่อไม่ได้ | ภาคผนวกอิทธิพล 8.5 |
| `powers.protect` | cost=35, cooldown_periods=4, mvp=ไม่ |  | พิทักษ์: หลัง MVP | ภาคผนวกอิทธิพล 8.6 |
| `powers.crisis_intervention` | cost=50, cooldown_periods=12, mvp=ไม่ |  | แทรกแซงวิกฤต: เปลี่ยนตายเป็นบาดเจ็บวิกฤต 1 ครั้ง/บท — หลัง MVP | ภาคผนวกอิทธิพล 8.7 |

## NPC: ความต้องการ ความทรงจำ ความสัมพันธ์

| คีย์ | ค่า | หน่วย | หมายเหตุ | ที่มา |
|---|---|---|---|---|
| `npc.need_urgent_on` | 75 | 0–100 | ความต้องการเกินค่านี้ = เร่งด่วน (hysteresis เปิด) | GDD เจาะลึก 5.2 (DECISIONS D9) |
| `npc.need_urgent_off` | 35 | 0–100 | ลดต่ำกว่าค่านี้ = หายเร่งด่วน (hysteresis ปิด) | GDD เจาะลึก 5.2 (DECISIONS D9) |
| `npc.memory_max_per_npc` | 25 | รายการ | ความทรงจำเด่นของ NPC สำคัญ (เอกสารให้ 20–30) | GDD เจาะลึก 5.7 |
| `npc.relationship_max_per_npc` | 30 | เส้น | เส้นความสัมพันธ์ละเอียดต่อคน (เอกสารให้ 20–40) | ภาคผนวกสังคม 13 |
| `npc.decision_softmax_temperature` | 0.15 |  | ความแปรผันตอนเลือก action ที่คะแนนใกล้กัน | ใหม่ — ต้องทดสอบ |

## ปาร์ตี้และการต่อสู้

| คีย์ | ค่า | หน่วย | หมายเหตุ | ที่มา |
|---|---|---|---|---|
| `party_combat.party_size_min` | 2 | คน |  | GDD เจาะลึก 7.1 |
| `party_combat.party_size_max` | 4 | คน |  | GDD เจาะลึก 7.1 |
| `party_combat.power_weight_combat_skill` | 0.45 |  | party_power = Σ(combat×0.45 + equipment×0.35 + health_ratio×20 + synergy×0.20) | GDD เจาะลึก 8.3 |
| `party_combat.power_weight_equipment` | 0.35 |  |  | GDD เจาะลึก 8.3 |
| `party_combat.power_weight_health_ratio` | 20 |  |  | GDD เจาะลึก 8.3 |
| `party_combat.power_weight_role_synergy` | 0.2 |  |  | GDD เจาะลึก 8.3 |
| `party_combat.risk_ratio_low_below` | 0.6 | risk_ratio | ต่ำกว่านี้ = เสี่ยงต่ำ | ใหม่ — ต้องทดสอบ |
| `party_combat.risk_ratio_medium_below` | 1.0 | risk_ratio | ต่ำกว่านี้ = ปานกลาง | ใหม่ — ต้องทดสอบ |
| `party_combat.risk_ratio_high_below` | 1.5 | risk_ratio | ต่ำกว่านี้ = สูง; ตั้งแต่ค่านี้ขึ้นไป = วิกฤต | ใหม่ — ต้องทดสอบ |

## เศรษฐกิจแบบย่อระดับชุมชน (DECISIONS D6)

| คีย์ | ค่า | หน่วย | หมายเหตุ | ที่มา |
|---|---|---|---|---|
| `economy.goods` | food, medicine, materials, equipment |  | สต็อกต่อชุมชน 4 หมวด + เงินของ NPC สำคัญ | GDD หลัก 8 / GDD เจาะลึก 6.2 |
| `economy.target_stock_days` | 7 | วัน | สต็อกเป้าหมายใช้คำนวณราคา | ภาคผนวกเศรษฐกิจ 7.2 |
| `economy.food_reserve_days` | 4 | วัน | อาหารสำรองชุมชน (เอกสารให้ 3–5) | ภาคผนวกเศรษฐกิจ 15.1 |
| `economy.price_exponent` | 0.25 |  | raw = base × (target/stock)^0.25 | ภาคผนวกเศรษฐกิจ 7.2 |
| `economy.price_index_min` | 0.6 | เท่าของฐาน |  | ภาคผนวกเศรษฐกิจ 7.2 |
| `economy.price_index_max` | 1.8 | เท่าของฐาน |  | ภาคผนวกเศรษฐกิจ 7.2 |
| `economy.price_daily_change_max` | 0.1 | สัดส่วน/วัน | ราคาขยับไม่เกิน ±10% ต่อวัน | ภาคผนวกเศรษฐกิจ 7.2 |
| `economy.shop_buy_ratio` | 0.9 | เท่าของราคาอ้างอิง | ร้านรับซื้อ (เอกสารให้ 0.85–0.95) | ภาคผนวกเศรษฐกิจ 7.1 |
| `economy.shop_sell_ratio` | 1.1 | เท่าของราคาอ้างอิง | ร้านขาย (เอกสารให้ 1.00–1.15) | ภาคผนวกเศรษฐกิจ 7.1 |
| `economy.constellation_production_bonus_cap` | 0.1 | สัดส่วน/กิจการ/วัน |  | ภาคผนวกเศรษฐกิจ 13 |

## พงศาวดาร (template อย่างเดียวใน MVP)

| คีย์ | ค่า | หน่วย | หมายเหตุ | ที่มา |
|---|---|---|---|---|
| `chronicle.importance_timeline` | 25 | คะแนน | ≥ ค่านี้ เก็บใน timeline บุคคล/พื้นที่ | ภาคผนวก Chronicle 4.3 |
| `chronicle.importance_notable` | 50 | คะแนน | ≥ ค่านี้ เป็น Notable Event | ภาคผนวก Chronicle 4.3 |
| `chronicle.importance_chronicle` | 75 | คะแนน | ≥ ค่านี้ เข้าพงศาวดารหลัก | ภาคผนวก Chronicle 4.3 |
| `chronicle.importance_era` | 90 | คะแนน | ≥ ค่านี้ เป็นหมุดหมายยุค ห้ามยุบรวม | ภาคผนวก Chronicle 4.3 |
| `chronicle.daily_digest_items` | 5 | รายการ | สรุปรายวัน 3–5 รายการ | ภาคผนวก Chronicle 9.1 |

## ขอบเขตโลก MVP

| คีย์ | ค่า | หน่วย | หมายเหตุ | ที่มา |
|---|---|---|---|---|
| `world_mvp.nodes` | 5 | โหนด | ลูเมน อัสเทรา ป่ารากเงิน เหมืองร้าง หอคอยจันทรา | GDD เจาะลึก 4.1 / 15.1 |
| `world_mvp.routes_max` | 7 | เส้น |  | GDD เจาะลึก 15.1 |
| `world_mvp.key_npcs` | 12 | คน |  | GDD เจาะลึก 15.1 |
| `world_mvp.monster_types` | 3 | ประเภท | + บอส 1 | GDD เจาะลึก 15.1 |
| `world_mvp.quest_types` | 5 | ประเภท |  | GDD เจาะลึก 15.1 |
| `world_mvp.chapter_crises` | 1 | วิกฤต/บท | ผลลัพธ์อย่างน้อย 3 แนวทาง | GDD เจาะลึก 10.3 / 15.1 |
| `world_mvp.stability_test_days` | 30 | วันเกม | โลกต้องเดินได้โดยไม่มีค่าหลุดขอบหรือวงจรค้าง | GDD เจาะลึก 16 |
