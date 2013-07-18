;; http://en.wikipedia.org/wiki/Contingent_vote

(define (cv-identify-losers results)
  (if (eq? results ()) ()
      (cv-id-losers-helper results ())))

(define (cv-id-losers-helper results losers)
  (if (eq? (length results) 2) 
      losers
      (let ((loser (car (trailer results))))
	(cons loser
	      (cv-id-losers-helper
	       (filter (lambda (x) (not (eq? loser (car x)))) results)
	       losers)))))

(define (cv-prune-losers losers votes)
  (if (eq? losers ()) 
      votes
      (cv-prune-losers 
       (cdr losers)
       (irv-disqualify (car losers) votes))))

(define (contingent-vote votes)
  (let* ((half (/ (length (irv-not-exhausted votes)) 2))
	 (firstround (tally (filter notfalse? (map irv-first-choice votes))))
	 (maybewinner (leader firstround)))
    (if (> (cdr maybewinner) half)
	(list firstround)
	(append
	 (contingent-vote (cv-prune-losers (cv-identify-losers firstround) votes))
	 (list firstround)))))

(define (contingent-restrict votes limit)
  (map
   (lambda (x)
     (if (> (length x) (length limit))
	 (map (lambda (y) (list-ref x y)) limit)
	 x))
   votes))

(define (supplementary-restrict votes)
  (contingent-restrict votes (list 0 1)))

(define (sri-lankan-contingent-restrict votes)
  (contingent-restrict votes (list 0 1 2)))
