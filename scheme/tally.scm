(define (notmypair x)
  (lambda (pair) (not (eq? x (car pair)))))

(define (tally votes)
  (if (eq? votes ())
      ()
      (let* ((thisvote (car votes))
	    (remaining (tally (cdr votes)))
	    (thiscount (assoc thisvote remaining)))
	(cons
	 (cons 
	  thisvote 
	  (if thiscount (+ 1 (cdr thiscount)) 1))
	 (filter (notmypair thisvote) remaining)))))

(define (weighted-tally votes)
  (if (eq? votes ())
      votes
      (let* ((this-weighted-vote (car votes))
	     (this-vote (car this-weighted-vote))
	     (this-weight (cdr this-weighted-vote))
	     (remaining-tally (weighted-tally (cdr votes)))
	     (this-vote-current-total (assoc this-vote remaining-tally)))
	(cons
	 (cons this-vote 
	       (if this-vote-current-total 
		   (+ this-weight (cdr this-vote-current-total))
		   this-weight))
	 (filter (notmypair this-vote) remaining-tally)))))

(define (tally votes)
  (weighted-tally (map (lambda (x) (cons x 1)) votes)))

(define (leader0 results comparator current-leader)
  (if (eq? results ())
      current-leader
      (let* ((biggest (cdr current-leader))
	    (contender (cdr (car results)))
	    (comparison (comparator contender biggest))
	    (next-leader (if comparison (car results) current-leader)))
	(leader0 (cdr results) comparator next-leader))))

(define (leader results)
  (leader0 results > (cons #f 0)))

(define (trailer results)
  (leader0 results < (car results)))

(define (notfalse? x) (not (false? x)))

(define (flatten-once x)
  (if (eq? x ()) x
      (append (car x) (flatten-once (cdr x)))))

(tally '(a b b c b a a a a c c b b b b c c c b a))
