# Finding limits that appear as silence

Read at steps 3-5. These questions exist because absent capability produces no error message and
no missing page — the question simply has no answer anywhere in the documentation, and reading
forward will never surface it.

## Model and representation

1. What distinction does our domain make that the core's model cannot hold?
2. Which of our states has no equivalent, and what does the core do with a record in that state?
3. Where do our enumerations and theirs partition the space differently? (Any place a mapping
   needs a default or "other" bucket is a gap, not a coding detail.)
4. Which of our concepts exists in the core only as free text?
5. Which relationships do we need that the core can only express in one direction?
6. What can exist in our domain but cannot be created in the core at all?

## Addressability

7. Which sub-objects have no identifier of their own?
8. What can we read but not write?
9. What can we write but not read back?
10. What must be rewritten whole because it cannot be addressed in parts?
11. Which records became unwritable because they entered under looser validation than the core now
    enforces?

## Queryability

12. Which fields can we not filter on? (Filters are hermetic — anything the resource does not
    physically carry cannot be filtered on, however derivable.)
13. What aggregate questions can the core not answer, forcing a full extract?
14. What history does the revision granularity make unanswerable?
15. Can we ask "what changed since X" at all, and against which clock?

## Operations and guarantees

16. Which operations fall outside the standard verb set, and what does each one's existence tell us
    about the model?
17. For each such operation, what does it guarantee? (Assume nothing carries over.)
18. Which business operations require several calls, and what is the state in between?
19. Which operations cannot be tested without performing them?
20. Which operations cannot be undone?
21. Which operations leave no record that they occurred?

## Timing and volume

22. Is there a bulk path distinct from the incremental one? If not, how does a cold start work?
23. What is the largest volume anyone has actually run through this, and where did it break?
24. What is the smallest interval at which we can ask for changes?
25. What happens to work in flight during a vendor upgrade?

## Contract and commercial

26. What is contracted in writing, as against described in documentation?
27. What notice do we get before a breaking change, and has that policy ever been exercised?
28. Which of the things we depend on are, in the vendor's view, internal?
29. What does the support agreement cover when the core is *slow* rather than down?
30. Which limits are commercial rather than technical, and therefore negotiable?

Question 30 is worth asking early and often. A limit that turns out to be a licensing tier rather
than an engineering constraint changes the whole conversation, and vendors rarely volunteer which
is which.
