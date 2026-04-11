% Format: pattern(Slot, Day, Period, CourseID, Type).
% 1st Bimester
pattern(1, mon, q(1,a), de, lecture).
pattern(2, mon, q(1,a), rp, lecture).
pattern(3, mon, q(1,a), rp, lab).
pattern(1, mon, q(1,a), bde, lecture).
pattern(2, mon, q(1,a), bde, lecture).

pattern(1, tue, q(1,a), aif, lab).
pattern(2, tue, q(1,a), ml1, lab).
pattern(3, tue, q(1,a), ml1, lecture).
pattern(2, tue, q(1,a), tm, lecture).
pattern(3, tue, q(1,a), aih, lecture).

pattern(1, wed, q(1,a), de, lab).
pattern(2, wed, q(1,a), nlu, lecture).
pattern(3, wed, q(1,a), nlu, lab).
pattern(2, wed, q(1,a), cog, lecture).
pattern(3, wed, q(1,a), cyb, lecture).

pattern(2, thu, q(1,a), aif, lecture).
pattern(3, thu, q(1,a), aif, lab).
pattern(2, thu, q(1,a), iot, lecture).
pattern(3, thu, q(1,a), eeai, lecture).

% 2nd Bimester
pattern(2, mon, q(1,b), rp, lecture).
pattern(3, mon, q(1,b), rp, lab).
pattern(1, mon, q(1,b), bde, lecture).
pattern(2, mon, q(1,b), bde, lecture).

pattern(1, tue, q(1,b), cv1, lecture).
pattern(2, tue, q(1,b), ml1, lab).
pattern(3, tue, q(1,b), ml1, lecture).
pattern(2, tue, q(1,b), tm, lecture).
pattern(3, tue, q(1,b), aih, lecture).

pattern(1, wed, q(1,b), cv1, lab).
pattern(2, wed, q(1,b), nlu, lecture).
pattern(3, wed, q(1,b), nlu, lab).
pattern(2, wed, q(1,b), cog, lecture).
pattern(3, wed, q(1,b), cyb, lecture).

pattern(2, thu, q(1,b), ir1, lecture).
pattern(3, thu, q(1,b), ir1, lab).
pattern(2, thu, q(1,b), iot, lecture).
pattern(3, thu, q(1,b), eeai, lecture).

% 3rd Bimester
pattern(1, mon, q(2,a), dl, lecture).
pattern(2, mon, q(2,a), aipm, lecture).
pattern(3, mon, q(2,a), aipm, lab).

pattern(1, tue, q(2,a), ec, lecture).
pattern(1, tue, q(2,a), kru, lecture).
pattern(2, tue, q(2,a), txai, lecture).
pattern(3, tue, q(2,a), txai, lab).

pattern(1, wed, q(2,a), ec, lab).
pattern(1, wed, q(2,a), kru, lab).
pattern(2, wed, q(2,a), mas, lecture).
pattern(3, wed, q(2,a), mas, lab).
pattern(2, wed, q(2,a), wist, lecture).
pattern(3, wed, q(2,a), wist, lab).

pattern(1, thu, q(2,a), dl, lab).
pattern(2, thu, q(2,a), ir2, lecture).
pattern(3, thu, q(2,a), ir2, lab).
pattern(2, thu, q(2,a), ml2, lecture).
pattern(3, thu, q(2,a), ml2, lab).

pattern(1, fri, q(2,a), mas, lecture).
pattern(2, fri, q(2,a), mas, lab).

% 4th Bimester
pattern(1, mon, q(2,b), dl, lecture).
pattern(2, mon, q(2,b), pm, lecture).
pattern(3, mon, q(2,b), pm, lab).

pattern(1, tue, q(2,b), irts, lecture).
pattern(2, tue, q(2,b), lm, lecture).
pattern(3, tue, q(2,b), lm, lab).
pattern(2, tue, q(2,b), ir2, lecture).
pattern(3, tue, q(2,b), ir2, lab).

pattern(1, wed, q(2,b), irts, lab).
pattern(2, wed, q(2,b), cv2, lecture).
pattern(3, wed, q(2,b), cv2, lab).
pattern(2, wed, q(2,b), wist, lecture).
pattern(3, wed, q(2,b), wist, lab).

pattern(1, thu, q(2,b), dl, lab).

pattern(1, fri, q(2,b), cv2, lecture).
pattern(2, fri, q(2,b), cv2, lab).

% Format: class(Slot, DD, MM, YYYY, Period, Course, Type).
class(S, D, M, Y, P, C, T) :-
    not holiday(D, M, Y),
    not mutant(D, M, Y, _),
    day(Day, D, M, Y),
    bimester_start(P, Ds, Ms, Ys),
    bimester_end(P, De, Me, Ye),
    (Y,M,D) >= (Ys,Ms,Ds),
    (Y,M,D) <= (Ye,Me,De),
    pattern(S, Day, P, C, T).

class(S, D, M, Y, P, C, T) :-
    mutant(D, M, Y, Day),
    not holiday(D, M, Y),
    bimester_start(P, Ds, Ms, Ys),
    bimester_end(P, De, Me, Ye),
    Y*10000 + M*100 + D >= Ys*10000 + Ms*100 + Ds,
    Y*10000 + M*100 + D <= Ye*10000 + Me*100 + De,
    pattern(S, Day, P, C, T).
