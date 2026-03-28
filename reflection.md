# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For my initial design, I identified three main user actions. First, the user should be able to add and manage pets, including storing basic information like the pet's name, species, age, and preferences. Second, the user should be able to create care tasks such as feedings, walks, medications, and appointments. And lastly the user should be able to generate a daily schedule that organizes these tasks by priority, timing, and owner preferences. The four main classes would be Owner, Pet, Task, and Scheduler. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing my first class skeleton, I made a few design improvements. I added a scheduled_date field to the Task class so the scheduling system would better support daily planning instead of only storing a vague preferred time. I also removed task-level conflict logic from Task because I realized conflict detection belongs more naturally in the Scheduler class, where all tasks can be compared together. Finally, I updated the Scheduler design to store an Owner instance so that scheduling behavior feels more connected to the specific owner's pets, preferences, and tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
