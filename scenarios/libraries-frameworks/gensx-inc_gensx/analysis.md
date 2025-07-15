# GenSX - Libraries & Frameworks Example

## Repository Information
**Repository:** https://github.com/gensx-inc/gensx  
**CLAUDE.md File:** https://github.com/gensx-inc/gensx/blob/main/CLAUDE.md  
**Description:** The TypeScript framework for agents & workflows with react-like components. Lightning fast dev loop. Easy to learn. Easy to extend.  
**Stars:** 200+ ⭐  

## Category: Libraries & Frameworks

## Why This Example Was Selected

This CLAUDE.md file exemplifies the **Libraries & Frameworks** category with several standout characteristics:

### 1. **Monorepo Architecture Guidance**
The file provides clear guidance for working with a complex monorepo structure:
- Package management with pnpm workspaces
- Build commands that work across multiple packages
- Testing strategies for interconnected components
- Clear distinction between packages/ and examples/ directories

### 2. **Framework-Specific Development Patterns**
GenSX is a TypeScript framework for AI agents, and the CLAUDE.md reflects this specialized domain:
- React-like component patterns with JSX syntax
- Specific import source configuration (@gensx/core as jsxImportSource)
- TypeScript-first development with strict typing requirements
- Agent and workflow development paradigms

### 3. **Developer Experience Focus**
The file emphasizes workflow efficiency:
- Mandatory linting fixes after code changes
- Automated formatting requirements
- Clear testing patterns for each package
- Development server setup for rapid iteration

### 4. **Code Quality Enforcement**
Strong emphasis on maintainable code:
- Explicit prohibition of `any` types
- Consistent naming conventions (camelCase vs PascalCase)
- Import organization with simple-import-sort
- Error handling patterns with specific error types

### 5. **Workflow Reminders**
Includes practical development reminders:
- Always run `pnpm lint:fix` after changes
- Documentation update requirements for API changes
- Specific guidance about commit messages

## Key Takeaways for claude.md Best Practices

1. **Architecture-Aware Commands**: Provide commands that understand the project's architectural complexity (monorepo, packages, etc.)
2. **Framework Conventions**: Document domain-specific patterns that are unique to the framework being developed
3. **Developer Workflow Integration**: Include reminders and requirements that prevent common mistakes
4. **Quality Gates**: Clearly specify code quality requirements and automated checks
5. **Scaling Considerations**: Address how development practices work across multiple packages/modules

This example shows how a claude.md for a framework should bridge the gap between general development practices and the specific paradigms that the framework introduces, making it easier for contributors to work effectively within the framework's conventions.