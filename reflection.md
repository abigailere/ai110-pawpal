# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
    - I thought of creating an owner, pet, tasks, and sceduler class. the owner will have its name, time availability, and a list of pet objects. Each pet will have a list of task object and each task will havea  title, duration, priority and if it is done or not. The scheduler will manage tasks by taking in its lists
    - after asking if there was anything to change, it suggested making a "low, "medium" and "high" priority have numerical weights to them for easier comparison and have the owner know about the scueduler. I made the change for priority but told it to add the other suggestions to the core features file as reminders when developing my code

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    - yes, the biggest one was how Owner stores pets. Originally it was just a list but I changed it to a private dictionary keyed by pet name so that checking for duplicates would be O(1) instead of scanning the whole list every time. It still looks like a list from the outside because of the property but internally its a dict
    - Task also got a lot more fields added to it. the original only had title, duration, priority and is_done but I added pet_name, recurrence, due_date, and start_time. recurrence and due_date came from wanting to support daily and weekly tasks that auto-reset when marked done. Start_time was added so the scheduler could actually detect if two tasks were overlapping in time
    - mark_complete() was added to Task so that when you complete a recurring task it handles creating the next one itself and returns it. That felt cleaner than putting that logic somewhere else
    - The Scheduler got three new methods that werent in the original design. sort_by_time() so you could sort by duration instead of just priority, detect_conflicts() to catch overlapping tasks, and complete_task() to wire mark_complete() into the right pet's task list automatically
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
    - The constraints i implemented were availability, priority, start time, and due date
    - I thought priority and time available were whiat mattered most because that would determine how I schedule the tasks and which ones will not be scheduled
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
    - when determining whether to add a task to the scheduler, my algorithm will always pick the highest priority regardless of how long it will take, meaning it would skip lower shorter tasks. I chose to do this because realistically, if something needs to be done for the health of a pet, an owner would consider that more important even if it would take longer
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
    - I used AI to help with brainstorming and refactoring. I came up with some general ideas I wanted and used claude code to check whether what I thought of was accurate given the requirements specified for the project as well as using it for suggesting things I missed. I also used it to generate the functions one by one so that I could look over it and check whether it made sense and test it individually. This helped with debugging because it made it easier to figure out which functions might be failing. I asked it what tests and functions meant.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
    - When asking it for clearer code, the generated code had more markdown and labels. Technically this would make it easier for a person to know what each line is doing, but when I looked over it, it made the entire section look cluttered, so the extra context was lost. AI understands redability in a binary way: is each part labeled with what it is doing, but it cannot tell if the whole makes sense because it cannot actually read.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
    - I tested the ability to add duplicate pets (pets with the same name), sort by time and priority, and if a task is set back to back (start of one task is the end of another) it would not be marked as overlapping. i thought these were important because having duplicate pets could make it hard to assign tasks to the right object. Ruling out the edge case of back to back scheduling is important because ti helps to accurately represent what can be done in a day for a user
**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
    - I am confident that my scheduler works as intended. All necessary features for a scheduler related to pet care are considered. If I had more time I would test if a task's time was embedded in another and see I could handle that in the scheduler. For example, if one task is from 8-9 and another is 8:15-8:30

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - I am most satisfied with the way my UI is set up when organizing tasks for each pet. Each pet has a name and an emoji to give a quick glance of their species. I also display how many tasks a pet has so a user will be able to quickly see how much needs to be done for their pets in a day
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - Because my project set a hard line for overlapping tasks, it does not allow duplication at all even though some tasks in real life can be done at the same time, for example feeding your pets. If I did this again I would add some way to give that algorithm context for a task so that it can reasonably schedule tasks more fit for real life
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - This project helped me improve my organization when I need the AI to do multiple things that may not be related to eachother. I was able to put general notes and things to keep in mind in a separate file so that I don't have to constantly scroll through the chat to find what I need. I also separated tasks into different chats so it wouldn.t get cluttered and I titled them so I knew what was where. For my future personal projects, I will definately be using the approach of separating notes into a different file for my reference
