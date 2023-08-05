$PROBLEM    PHENOBARB SIMPLE MODEL
$INPUT      ID DV MDV OPRED D_EPS1 TIME AMT WGT APGR D_ETA1 D_ETA2
            OETA1 OETA2 D_EPSETA1_1 D_EPSETA1_2
$DATA      ../pheno_linbase.dta IGNORE=@ IGNORE(MDV.NEN.0)
$PRED
BASE1=D_ETA1*(ETA(1)-OETA1)
BASE2=D_ETA2*(ETA(2)-OETA2)
BSUM1=BASE1+BASE2
BASE_TERMS=BSUM1
IPRED=OPRED+BASE_TERMS
ERR1=EPS(1)*(D_EPS1+D_EPSETA1_1*(ETA(1)-OETA1))
ERR2=EPS(1)*(D_EPSETA1_2*(ETA(2)-OETA2))
ESUM1=ERR1+ERR2
ERROR_TERMS=ESUM1
Y=IPRED+ERROR_TERMS
$OMEGA  BLOCK(2)
 0.111053
 0.00149599688763045 0.201526
$SIGMA  0.0164177
$ESTIMATION METHOD=COND INTERACTION MAXEVALS=9999999 PRINT=1 MCETA=10
$COVARIANCE OMITTED
