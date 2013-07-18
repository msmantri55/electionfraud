;; http://en.wikipedia.org/wiki/Borda_count

(define (borda-transform-one vote)
  (if (eq? vote ()) 
      vote
      (append (make-list (length vote) (car vote))
	      (borda-transform-one (cdr vote)))))

(define (borda-one-tally votes)
  (tally (flatten-once (map borda-transform-one votes))))

(define (borda-transform-zero vote)
  (let ((n (length vote)))
    (if (< n 2) 
	()
	(append (make-list (- n 1) (car vote))
		(borda-transform-zero (cdr vote))))))

(define (borda-zero-tally votes)
  (tally (flatten-once (map borda-transform-zero votes))))

(define (borda-modified-transform candidates)
  (lambda (vote)
    (append (make-list (- candidates (length vote)) #f) vote)))

(define (borda-modified-tally votes candidates)
  (filter 
   (notmypair #f)
   (tally 
    (flatten-once 
     (map (borda-modified-transform candidates) votes))))
  
(define (borda-transform-nauru-helper vote position candidates)
  (if (eq? vote ())
      vote
      (cons
       (cons (car vote) (/ 1 position))
       (borda-transform-nauru-helper (cdr vote) (+ position 1) candidates))))

(define (borda-transform-nauru vote)
  (borda-transform-nauru-helper vote 1 (length vote)))

(define (borda-nauru-tally votes)
  (weighted-tally (flatten-once (map borda-transform-nauru votes))))
