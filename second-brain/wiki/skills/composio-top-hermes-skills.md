---
title: Top Hermes Skills from Composio
type: source_summary
date: 2026-05-17
sources: raw/inbox/2026-05-17-composio-skills-summary.md
related: "[[hermes-openclaw-noa-agent]]"
---

# Top Hermes Skills from Composio Article

Dit document vat de meest nuttige Hermes skills samen, gebaseerd op een analyse van het artikel "Best Hermes Agent Skills I’d Reinstall Immediately" van Composio. Deze skills zijn bijzonder relevant voor de verdere ontwikkeling en operationele efficiëntie van Noa.

## Belangrijkste aanbevolen skills voor Noa:

### 1. Obsidian Skills
*   **Beschrijving:** Verbetert de interactie met de kennisbank (second brain) voor geavanceerd kennisbeheer.
*   **Relevantie voor Noa:** Helpt bij het gestructureerd gebruiken en ophalen van informatie uit onze bestaande kennisbasis.
*   **Installatie (referentie uit artikel):** `npx skills add aaron-he-zhu/seo-geo-claude-skills --target ~/.hermes/skills`

### 2. Claudeception
*   **Beschrijving:** Versterkt de leerlus van Hermes door geleerde kennis als zelfverbeterende skills op te slaan, met optimisatie voor toekomstige oproepen.
*   **Relevantie voor Noa:** Cruciaal voor eigen ontwikkeling, leren van successen en directe hergebruik van kennis.
*   **Installatie (referentie uit artikel):** `git clone https://github.com/blader/Claudeception.git ~/.hermes/skills/claudeception`

### 3. Reflexion
*   **Beschrijving:** Implementeert een zelfcorrectie-lus; de agent evalueert en verbetert zijn eigen output voor hogere kwaliteit.
*   **Relevantie voor Noa:** Direct toepasbaar om de kwaliteit van antwoorden en acties te verbeteren via een ingebouwde kwaliteitscontrole.
*   **Installatie (referentie uit artikel):** `npx skills add NeoLabHQ/reflexion --target ~/hermes/skills`

## Andere nuttige concepten en skills:

*   **Obra Superpowers:** Gericht op "Operating Discipline" voor gestructureerde taakuitvoering.
*   **Composio Universal CLI + Skill:** Biedt een "Integration Layer" voor het koppelen van tools en systemen.
*   **Playwright Skill:** Biedt productietests voor automatisering.
*   **Humanizer:** Helpt bij het verwijderen van "AI-tell" uit tekst, wat tekst natuurlijker maakt.

## Veiligheidswaarschuwing:
Het artikel benadrukt het belang van voorzichtigheid: "Vet anything you grab from a random repo. ... Read the SKILL.md before you install." Dit is een cruciale richtlijn bij het installeren van nieuwe code in de omgeving van de agent.

---
 Bron: https://composio.dev/content/best-hermes-skills