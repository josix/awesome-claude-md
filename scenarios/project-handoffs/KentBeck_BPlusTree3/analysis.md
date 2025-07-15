# Analysis: Kent Beck's TDD-Focused CLAUDE.md

**Category: Project Handoffs**  
**Source**: [KentBeck/BPlusTree3](https://github.com/KentBeck/BPlusTree3)  
**CLAUDE.md**: [View Original](https://github.com/KentBeck/BPlusTree3/blob/main/rust/docs/CLAUDE.md)  
**Additional**: [System Prompt Additions](https://github.com/KentBeck/BPlusTree3/blob/main/.claude/system_prompt_additions.md)  
**License**: MIT License  

This CLAUDE.md file from Kent Beck's BPlusTree3 project exemplifies how to onboard an AI assistant to specific development methodologies and project-specific workflows.

## Key Features That Make This Exemplary

### 1. **Methodology-First Approach**
- Establishes the AI's role as a "senior software engineer" following specific principles
- Clearly defines TDD cycle (Red → Green → Refactor)
- Emphasizes "Tidy First" separation of structural vs behavioral changes

### 2. **Precise Workflow Instructions**
- References external documentation (`plan.md`) for task sequencing
- Uses imperative commands like "When I say 'go', find the next unmarked test"
- Specifies exact behavior: "implement only enough code to make that test pass"

### 3. **Quality Gates and Discipline**
- Lists specific commit requirements (all tests passing, no warnings)
- Mandates clear commit message conventions
- Enforces small, frequent commits over large ones

## Unique Techniques

### **External Reference Integration**
Unlike generic guidance, this file references project-specific documentation (`plan.md`), creating a bridge between the AI and existing project workflows.

### **Behavioral Constraints**
The file doesn't just describe what to do—it constrains *how* to do it, preventing the AI from taking shortcuts that violate TDD principles.

### **Role-Based Instructions**
By establishing the AI as a "senior software engineer," it sets expectations for the level of expertise and decision-making required.

## Key Takeaways

1. **Methodology Over Technology**: Focus on development process rather than technical stack
2. **Reference External Docs**: Link to existing project documentation for dynamic guidance
3. **Enforce Discipline**: Use explicit constraints to ensure AI follows established practices

This approach demonstrates how CLAUDE.md can serve as both onboarding documentation and a behavioral contract for AI assistance in methodical development practices.