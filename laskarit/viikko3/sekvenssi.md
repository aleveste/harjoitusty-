## Sekvenssikaavio

```mermaid
sequenceDiagram
    participant Main
    participant HKLLaitehallinto
    participant Lataajalaite as Rautatietori
    participant Lukijalaite1 as Ratikka6
    participant Lukijalaite2 as Bussi244
    participant Kioski
    participant Matkakortti as Kallen kortti
    
    Main->>HKLLaitehallinto: __init__()
    Main->>Lataajalaite: __init__()
    Main->>Lukijalaite1: __init__()
    Main->>Lukijalaite2: __init__()
    Main->>HKLLaitehallinto: lisaa_lataaja(rautatietori)
    Main->>HKLLaitehallinto: lisaa_lukija(ratikka6)
    Main->>HKLLaitehallinto: lisaa_lukija(bussi244)
    
    Main->>Kioski: osta_matkakortti("Kalle")
    Kioski->>Matkakortti: __init__("Kalle")
    Kioski-->>Main: Kallen kortti
    
    Main->>Lataajalaite: lataa_arvoa(Kallen kortti, 3)
    Lataajalaite->>Matkakortti: kasvata_arvoa(3)
    
    Main->>Lukijalaite1: osta_lippu(Kallen kortti, 0)
    Lukijalaite1->>Matkakortti: vahenna_arvoa(1.5)
    
    Main->>Lukijalaite2: osta_lippu(Kallen kortti, 2)
    Lukijalaite2->>Matkakortti: vahenna_arvoa(3.5)