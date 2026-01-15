# 🤝 Contributing to Scientific AI Engineering Curriculum

Thank you for considering contributing to this educational project! This curriculum aims to be a community-driven resource for learning Scientific AI Engineering and Building Performance Simulation.

---

## 📋 Table of Contents

- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Contribution Guidelines](#contribution-guidelines)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

---

## 🎯 How Can I Contribute?

### **1. Report Issues**
Found a bug in code examples? Exercise instructions unclear?

- Check if the issue already exists in [Issues](../../issues)
- If not, create a new issue with:
  - Clear title (e.g., "Exercise 5.2: Missing import statement")
  - Location (Month, Week, Exercise)
  - Description of the problem
  - Expected vs actual behavior
  - Your environment (Python version, OS, etc.)

### **2. Improve Documentation**
Documentation improvements are highly valued!

- Fix typos or grammar
- Clarify confusing explanations
- Add missing prerequisites
- Improve code comments
- Translate to other languages

### **3. Enhance Code Examples**
Make examples better, clearer, or more robust:

- Add error handling
- Improve code comments
- Optimize performance
- Add type hints
- Include additional test cases

### **4. Add New Content**
Contribute new exercises or case studies:

- Alternative implementations
- Industry-specific case studies
- Regional adaptations (climate zones, building codes)
- Integration with additional tools
- Advanced variations of existing exercises

### **5. Share Your Experience**
Help future learners:

- Document challenges and solutions
- Share tips and best practices
- Contribute real-world datasets (properly licensed)
- Create video tutorials or walkthroughs

---

## 🚀 Getting Started

### **1. Fork & Clone**

```bash
# Fork this repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/ai-engineering-curriculum.git
cd ai-engineering-curriculum

# Add upstream remote
git remote add upstream https://github.com/joao-petreche/ai-engineering-curriculum.git
```

### **2. Create a Branch**

```bash
# Create a descriptive branch name
git checkout -b fix/exercise-5-2-import-error
# or
git checkout -b docs/improve-mes3-readme
# or
git checkout -b feature/add-pytorch-alternative
```

### **3. Set Up Environment**

```bash
# Follow setup instructions in the relevant month
cd "Science AI Engineering"
# Install dependencies as specified in Exercicios_Mes_0_Setup.md
```

---

## 📝 Contribution Guidelines

### **General Principles**

✅ **DO:**
- Keep changes focused and atomic (one issue per PR)
- Test your code changes thoroughly
- Update related documentation
- Follow existing structure and naming conventions
- Be respectful and constructive in discussions
- Give credit to sources and references

❌ **DON'T:**
- Make massive refactors without discussion
- Break existing functionality
- Add dependencies without justification
- Include copyrighted material without permission
- Mix multiple unrelated changes in one PR

### **Content Quality Standards**

**For Code:**
- ✅ Tested and working
- ✅ Well-commented (explain "why", not just "what")
- ✅ Follows PEP 8 (Python) or language conventions
- ✅ Includes error handling for common cases
- ✅ Uses meaningful variable names

**For Documentation:**
- ✅ Clear and concise language
- ✅ Proper markdown formatting
- ✅ Includes examples where helpful
- ✅ Accessible to target audience (graduate level)
- ✅ Free of jargon (or jargon is explained)

**For Exercises:**
- ✅ Clear learning objectives
- ✅ Realistic time estimates
- ✅ Appropriate difficulty progression
- ✅ Complete starter code and solutions
- ✅ Validation criteria

---

## 🎨 Code Style

### **Python Code**

Follow **PEP 8** with these specifics:

```python
# Imports: grouped and sorted
import os
import sys

import numpy as np
import pandas as pd

from local_module import LocalClass

# Constants: UPPER_CASE
MAX_ITERATIONS = 1000
DEFAULT_TEMPERATURE = 20.0

# Functions: snake_case with docstrings
def calculate_energy_consumption(
    temperature: float,
    setpoint: float,
    efficiency: float = 0.85
) -> float:
    """
    Calculate building energy consumption based on temperature difference.
    
    Args:
        temperature: Current outdoor temperature (°C)
        setpoint: Indoor temperature setpoint (°C)
        efficiency: System efficiency (0-1)
    
    Returns:
        Energy consumption in kWh
    """
    delta_t = abs(temperature - setpoint)
    return delta_t * (1 / efficiency) * CONVERSION_FACTOR

# Classes: PascalCase
class BuildingSimulator:
    """Simulate building thermal behavior."""
    
    def __init__(self, config: dict):
        self.config = config
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Private method for internal validation."""
        pass
```

### **Markdown Documentation**

```markdown
# Main Heading (H1) - One per document

Brief introduction paragraph.

## Section Heading (H2)

Content with proper spacing.

### Subsection (H3)

- Bullet points with proper capitalization
- Use **bold** for emphasis
- Use `code` for technical terms

**Code blocks with language specified:**

```python
# Python example
import numpy as np
```

**Tables formatted consistently:**

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

### **File Naming Conventions**

- Exercises: `Exercicios_Mes_XX_Topic.md`
- Documentation: `UPPERCASE_WITH_UNDERSCORES.md`
- Scripts: `lowercase_with_underscores.py`
- Directories: `lowercase_with_underscores/`

---

## 📤 Submitting Changes

### **1. Commit Your Changes**

```bash
# Stage your changes
git add path/to/changed/files

# Write clear commit message
git commit -m "Fix: Correct import error in Exercise 5.2

- Added missing 'from typing import List' import
- Updated code example to use List type hint
- Tested on Python 3.9 and 3.10

Fixes #42"
```

**Commit Message Format:**

```
<type>: <short summary> (max 50 chars)

<detailed description if needed>
- Use bullet points for multiple changes
- Reference issue numbers with #

<footer: Fixes #issue-number>
```

**Types:** `Fix`, `Docs`, `Feature`, `Refactor`, `Test`, `Chore`

### **2. Push to Your Fork**

```bash
git push origin fix/exercise-5-2-import-error
```

### **3. Open a Pull Request**

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Fill out the PR template:

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] Documentation improvement
- [ ] New feature/content
- [ ] Refactoring

## Testing
Describe how you tested these changes:
- [ ] Tested code examples
- [ ] Reviewed documentation formatting
- [ ] Checked links

## Related Issues
Fixes #42

## Screenshots (if applicable)
[Add screenshots for UI/documentation changes]

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Changes are tested
- [ ] Commit messages are clear
```

---

## 🔍 Review Process

### **What to Expect**

1. **Automated Checks** (if configured):
   - Linting (code style)
   - Unit tests
   - Link validation

2. **Maintainer Review**:
   - Typically within 3-7 days
   - May request changes or clarifications
   - Constructive feedback provided

3. **Iteration**:
   - Address feedback
   - Push updates to same branch
   - PR updates automatically

4. **Merge**:
   - Once approved, maintainer merges
   - Your contribution is credited
   - Branch can be deleted

### **Review Criteria**

✅ **Approved if:**
- Solves stated problem
- Follows style guidelines
- Doesn't break existing functionality
- Documentation is clear
- Changes are tested

❌ **Changes requested if:**
- Code doesn't follow conventions
- Missing documentation
- Breaking changes without discussion
- Untested or broken functionality
- Scope creep (too many unrelated changes)

---

## 🌍 Translations

Interested in translating content?

1. Create issue: "Translation: [Language]"
2. Discuss structure with maintainers
3. Translate in batches (by month)
4. Maintain original filenames with language suffix:
   - `Exercicios_Mes_01_pt-BR.md`
   - `Exercicios_Mes_01_es.md`
   - `Exercicios_Mes_01_zh-CN.md`

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the **MIT License**, same as the project.

---

## ❓ Questions?

- 💬 Open a [Discussion](../../discussions)
- 📧 Email: petreche@usp.br
- 🐛 Report issues in [Issues](../../issues)

---

## 🙏 Recognition

All contributors will be recognized in:
- Repository contributors list
- CONTRIBUTORS.md file (significant contributions)
- Annual acknowledgment in project updates

Thank you for helping improve Scientific AI Engineering education! 🎓

---

**Happy Contributing!** 🚀
