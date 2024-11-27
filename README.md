# VisualQARest


Visual Answering mit Nutzung folgender Modelle:
-  [Aquila](https://huggingface.co/BAAI/Aquila-VL-2B-llava-qwen)
-  [Llava](https://huggingface.co/OpenFace-CQUPT/Human_LLaVA)
-  [VILT](https://huggingface.co/dandelin/vilt-b32-finetuned-vqa)
-  [Owl](https://github.com/X-PLUG/mPLUG-Owl/tree/main/mPLUG-Owl3)
 
## Einrichtung und Konfiguration:

Python: 3.10

Pycharm 2024.3 Community Version

0) Im Terminal den Befehl ```pip install -r requirements.txt```  ausführen
1) Siehe [Datei](Resources/geo_reference.ini)
2) Auswahl eines Modells im config ```model.type_model
3) [main.py](src/main.py) in **run config** als Startskript anlegen und starten
4) Warten bis das ausgewählte Modell heruntergeladen wurde (ansonsten Modelle aus share (/home/share/droptableteams/huggingface) in das eigene cache-Verzeichnis (//home/.cache) kopieren.
4) [API](http://127.0.0.1:9000/docs#/Visual%20Questioning/vaq_vaq_post) anfragen mit einem Text und einem Bild (per Try out)

