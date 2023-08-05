$SIZES      DIMNEW=-10000
$PROBLEM    PHENOBARB SIMPLE MODEL
$INPUT      ID DV MDV OPRED D_EPS1 TIME AMT WGT APGR D_ETA1 D_ETA2
            OETA1 OETA2 D_EPSETA1_1 D_EPSETA1_2
$DATA      ../pheno_linbase.dta IGNORE=@ IGNORE(MDV.NEN.0)
$PRED ETAT1 = ETA(1)*(1+((ETA(1)**2+1)/(4*THETA(1)))&
    +((5*ETA(1)**4+16*ETA(1)**2+3)/(96*THETA(1)**2))&
    +((3*ETA(1)**6+19*ETA(1)**4+17*ETA(1)**2-15)/(384*THETA(1)**3)))
ETAT2 = ETA(2)*(1+((ETA(2)**2+1)/(4*THETA(2)))&
    +((5*ETA(2)**4+16*ETA(2)**2+3)/(96*THETA(2)**2))&
    +((3*ETA(2)**6+19*ETA(2)**4+17*ETA(2)**2-15)/(384*THETA(2)**3)))

BASE1=D_ETA1*(ETAT1-OETA1)
BASE2=D_ETA2*(ETAT2-OETA2)
BSUM1=BASE1+BASE2
BASE_TERMS=BSUM1
IPRED=OPRED+BASE_TERMS
ERR1=EPS(1)*(D_EPS1+D_EPSETA1_1*(ETAT1-OETA1))
ERR2=EPS(1)*(D_EPSETA1_2*(ETAT2-OETA2))
ESUM1=ERR1+ERR2
ERROR_TERMS=ESUM1
Y=IPRED+ERROR_TERMS
$THETA  (3,80,100)
$THETA  (3,80,100)
$OMEGA  0.111053  ;       IVCL
$OMEGA  0.201526  ;        IVV
$SIGMA  0.0164177
$ESTIMATION METHOD=COND INTERACTION MAXEVALS=9999999 PRINT=1 MCETA=10
$COVARIANCE OMITTED
