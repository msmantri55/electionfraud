;; http://en.wikipedia.org/wiki/Instant-runoff_voting

(define (irv-dq-single-vote choice)
  (lambda (x) (not (eq? choice x))))

(define (irv-disqualify choice votes)
  (map
   (lambda (x)
     (filter (irv-dq-single-vote choice) x))
   votes))

(define (irv-exhausted? vote) (eq? vote ()))

(define (irv-not-exhausted votes) 
  (filter (lambda (x) (not (irv-exhausted? x))) votes))

(define (irv-first-choice vote)
  (if (irv-exhausted? vote) #f (car vote)))

(define (irv-round votes prevrounds)
  (let* ((half (/ (length (irv-not-exhausted votes)) 2))
	 (thisround (tally 
		     (filter notfalse? (map irv-first-choice votes))))
	 (maybewinner (leader thisround)))
    (if (> (cdr maybewinner) half)
	(cons thisround prevrounds)
	(let ((loser (car (trailer thisround))))
	  (irv-round
	   (irv-disqualify loser votes)
	   (cons thisround prevrounds))))))

(define (irv votes) (irv-round votes ()))

(irv tennessee-capital-election)
