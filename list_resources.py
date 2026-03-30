#!/usr/bin/env python3
import os
import glob
from datetime import datetime

print("=" * 60)
print("JESUS (CATHOLIC) CHATBOT - RESOURCE INVENTORY")
print("=" * 60)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Check documents folder
docs_folder = "/home/tony-cullen/catholic_chatbot/catholic_documents"
if os.path.exists(docs_folder):
    print("📚 LOCAL DOCUMENTS")
    print("-" * 40)
    
    categories = {
        "bible": "bible*.txt",
        "catechism": "catechism*.txt",
        "vatican": ["lumen_gentium.txt", "dei_verbum.txt", "gaudium_et_spes.txt", 
                    "sacrosanctum_concilium.txt", "apostolicam_actuositatem.txt", 
                    "ad_gentes.txt", "presbyterorum_ordinis.txt", "unitatis_redintegratio.txt", 
                    "nostra_aetate.txt"],
        "papal": ["laudato_si.txt", "fratelli_tutti.txt", "evangelii_gaudium.txt", 
                  "deus_caritas_est.txt", "spe_salvi.txt", "lumen_fidei.txt", 
                  "amoris_laetitia.txt", "veritatis_splendor.txt", "evangelium_vitae.txt",
                  "redemptor_hominis.txt", "dives_in_misericordia.txt"],
        "saints": "saint_*.txt",
        "mary": ["mary_*.txt", "marian_*.txt", "our_lady_*.txt", "rosary_*.txt"],
        "apostles": "apostle_*.txt",
        "eucharist": ["eucharistic_*.txt", "theology_eucharist.txt", "preparation_communion.txt", 
                      "eucharist_saints.txt", "corpus_christi.txt", "first_communion.txt"],
        "mass": "mass_*.txt",
        "camino": "camino_*.txt",
        "gospels": ["gospel_*.txt", "romans.txt", "genesis_ark.txt", "forgiveness.txt"],
        "social_teaching": ["social_teaching.txt", "noahs_ark_catholic.txt"],
        "other": ["depression_hope.txt", "prodigal_son.txt"]
    }
    
    for category, pattern in categories.items():
        files = []
        if isinstance(pattern, list):
            for p in pattern:
                files.extend(glob.glob(os.path.join(docs_folder, p)))
        else:
            files = glob.glob(os.path.join(docs_folder, pattern))
        
        if files:
            print(f"\n{category.upper()}:")
            for f in sorted(files):
                filename = os.path.basename(f)
                size = os.path.getsize(f)
                print(f"  • {filename} ({size:,} bytes)")
    
    # Count total
    all_files = glob.glob(os.path.join(docs_folder, "*.txt"))
    print(f"\n" + "=" * 60)
    print(f"TOTAL DOCUMENTS: {len(all_files)}")
else:
    print("⚠️  Documents folder not found")

print("\n" + "=" * 60)
print("🌐 WEB SEARCH DOMAINS (Catholic-approved)")
print("-" * 40)
print("vatican.va, usccb.org, ewtn.com, catholic.com, newadvent.org, ")
print("catholicculture.org, biblegateway.com, papalencyclicals.net, ")
print("catholiceducation.org, catholictradition.org, firstthings.com, ")
print("ignatius.com, scborromeo.org, catholicsaints.info, and more.")

print("\n" + "=" * 60)
print("🤖 CHATBOT FEATURES")
print("-" * 40)
print("✅ Local document search (40+ documents)")
print("✅ Web search (Catholic-approved domains)")
print("✅ OpenAI integration (GPT-3.5-turbo)")
print("✅ 'What Would Jesus Say?' perspective")
print("✅ Scripture references with Bible verses")
print("✅ How to Apply This Today section")
print("✅ Questions to Reflect On section")
print("✅ Closing prayer")
print("✅ Personal address (speaks directly to user)")
print("✅ Comprehensive Catholic resources")

print("\n" + "=" * 60)
