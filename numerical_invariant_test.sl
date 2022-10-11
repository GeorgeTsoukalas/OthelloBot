(set-logic BV)

(define-fun origFun ( (X Float) (Y Float) ) Bool 
		(and (hyp X) (hyp Y))
)

(synth-fun skel ( (X Float) (Y Float) ) Bool
		  ((Start Bool (
										  (and depth1 depth1)
										  (or depth1 depth1)
										  (affine X Y)
		  ))
		  (depth1 Bool (
										  (affine X Y)
		  )))
)

(declare-var X Float)
(declare-var Y Float)

(constraint (= (origFun X Y ) (skel X Y)))


(check-synth)