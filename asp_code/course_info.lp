% course(courseid,mandatory/optional,period,credits)
% %%%%% check credits values %%%%%

name(aif, "ai fundamentals").
name(de, "data engineering").
name(rp, "reasoning and planning").
name(nlu, "natural language understanding").
name(ml1, "machine learning 1").
name(cv1, "computer vision 1").
name(ir1, "intelligent robotics 1").

name(txai, "trustable and explainable ai").
name(mas, "multi-agent systems").
name(kru, "knowledge representation with uncertainty").
name(lm, "language modelling").
name(wist, "web intelligence and semantic technologies").
name(dl, "deep learning").
name(ml2, "machine learning 2").
name(ec, "evolutionary computation").
name(cv2, "computer vision 2").
name(ir2, "intelligent robotics 2").
name(aipm, "ai project management").
name(pm, "process mining").
name(irts, "intelligent real time systems").

name(cog, "computational aspects of cognitive systems").
name(tm, "text mining").
name(bde, "ai in big data environments").
name(iot, "intelligent iot").
name(cyb, "intelligent cybersecurity").
name(eeai, "emerging and entrepreneurial ai").
name(aih, "ai in health").

% Q1
course(rp,mandatory,(q(1,a);q(1,b)),6).
course(nlu,mandatory,(q(1,a);q(1,b)),6).
course(ml1,mandatory,(q(1,a);q(1,b)),6).

course(aif,mandatory,q(1,a),3).
course(de,mandatory,q(1,a),3).
course(cv1,mandatory,q(1,b),3).
course(ir1,mandatory,q(1,b),3).

%Q2
course(dl,optional,(q(2,a);q(2,b)),6).
course(ir2,optional,q(2,b),6).
course(wist,optional,q(2,b),6).

course(txai,mandatory,q(2,a),3).
course(aipm,mandatory,q(2,a),3).
course(kru,optional,q(2,a),3).
course(ec,optional,q(2,a),3).
course(ml2,optional,q(2,a),3).
course(mas,optional,q(2,a),6).
course(pm,optional,q(2,b),3).
course(irts,optional,q(2,b),3).
course(lm,optional,q(2,b),3).
course(cv2,optional,q(2,b),6).

% Q3
course(cog,optional,(q(1,a);q(1,b)),3).
course(tm,optional,(q(1,a);q(1,b)),3).
course(bde,optional,(q(1,a);q(1,b)),6).
course(iot,optional,(q(1,a);q(1,b)),3).
course(cyb,optional,(q(1,a);q(1,b)),3).
course(eeai,optional,(q(1,a);q(1,b)),3).
course(aih,optional,(q(1,a);q(1,b)),3).
