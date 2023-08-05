$PROBLEM    PHENOBARB SIMPLE MODEL
$DATA      pheno.dta IGNORE=@
$INPUT      ID TIME AMT WGT APGR DV
$SUBROUTINE ADVAN1 TRANS2
$PK
CL=THETA(1)*EXP(ETA(1))
V=THETA(2)*EXP(ETA(2))
S1=V

$ERROR
Y=F+F*EPS(1)

$THETA  (0,0.00581756) ; TVCL
$THETA  (0,1.44555) ; TVV
$OMEGA  0.111053  ;       IVCL
$OMEGA  0.201526  ;        IVV
$SIGMA  0.0164177
$SIMULATION (217420) SUBPROB=1
$ESTIMATION METHOD=1 INTERACTION MAXEVALS=0
$TABLE      ID DV MDV CWRES NOPRINT NOAPPEND ONEHEADER
            FILE=sim_res_table-3.dta

