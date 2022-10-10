(set-logic BV)

(define-fun origFun ( (X Float) (Y Float) ) Bool 
		(and (hyp (OrigFun1 X Y)) (hyp (OrigFun2 X Y)))
)

(synth-fun skel ( (X Float) (Y Float) ) Bool
		  ((Start Bool (
										  (and depth1 depth1)
										  (or depth1 depth1)
										  (hyp func)
		  ))
		  (depth1 Bool (
										  (hyp func)
		  ))
		  (func Float  (
										  (affine X Y)
		  )))
)

(declare-var X Float)
(declare-var Y Float)

(constraint (= (origFun X Y ) (skel X Y)))


(check-synth)
