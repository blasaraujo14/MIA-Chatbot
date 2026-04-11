month(jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec).
week_day(mon, tue, wed, thu, fri).

% Slots 1, 2 and 3 are for classes, slots 4 and 5 are for exams.
% Format: slot_time(Slot, StartTime, EndTime).
slot_time(1, "15:30", "17:00").
slot_time(2, "17:00", "18:30").
slot_time(3, "18:30", "20:00").
slot_time(4, "10:30", "13:30").
slot_time(5, "16:00", "19:00").

% Format: bimester_start(Period, DD, MM, YYYY).
bimester_start(q(1,a), 8, 9, 2025).
bimester_start(q(1,b), 27, 10, 2025).
bimester_start(q(2,a), 27, 1, 2026).
bimester_start(q(2,b), 13, 4, 2026).

% Format: bimester_end(Period, DD, MM, YYYY).
bimester_end(q(1,a), 23, 10, 2025).
bimester_end(q(1,b), 15, 12, 2025).
bimester_end(q(2,a), 24, 3, 2026).
bimester_end(q(2,b), 2, 6, 2026).

% Format: holiday(DD, MM, YYYY).
holiday(11, 11, 2025).
holiday(8, 12, 2025).
holiday(30, 1, 2026).
holiday(16, 2, 2026).
holiday(17, 2, 2026).
holiday(18, 2, 2026).
holiday(19, 3, 2026).
holiday(20, 3, 2026).
holiday(17, 4, 2026).
holiday(1, 5, 2026).
holiday(14, 5, 2026).

% Format: mutant(DD, MM, YYYY, week_day).
mutant(14, 11, 2025, tue).
mutant(24, 3, 2026, fri).
mutant(1, 6, 2026, fri).
mutant(2, 6, 2026, thu).