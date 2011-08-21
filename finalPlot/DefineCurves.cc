#include "ExclusionPlot.hh"

TGraphErrors* get250Obs(){

  Int_t nl = 10;
  Double_t xl[10]={ 50,150,250,350,450,550,650,750,850,950};
  Double_t yl[10]={450,450,430,420,390,310,240,200,190,180};
  Double_t exl[10];
  Double_t eyl[10];

  TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
  gr1->SetMarkerColor(kBlue);
  gr1->SetMarkerStyle(21);

  //gr1->Draw("LP");

  TSpline3 *s = new TSpline3("grs",gr1);
  s->SetLineColor(kBlue);
  s->SetLineStyle(2);
  s->SetLineWidth(3);

  return gr1;

}

// TGraphErrors* getPL(){

//   Int_t nl = 21;
//   Double_t xl[21]={0,   100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000};
//   Double_t yl[21]={260, 400, 360, 320, 340, 360, 240, 180, 170, 140, 140,  140,  120,  120,  140,  120,  100,  100,  100,  80,   0};
//   Double_t exl[21];
//   Double_t eyl[21];

//   TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
//   gr1->SetMarkerColor(kBlue);
//   gr1->SetMarkerStyle(21);

//   //gr1->Draw("LP");

//   TSpline3 *s = new TSpline3("grs",gr1);
//   s->SetLineColor(kBlue);
//   s->SetLineStyle(2);
//   s->SetLineWidth(3);

//   return gr1;

// }

TGraphErrors* get1fbObs_LO(){
  Int_t nl = 21-9;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, /*700,*/ 800, /*900,*/ 1000, /*1100,*/ 1200, /*1300, 1400,*/ 1500, /*1600, 1700,*/ 1800, /*1900,2000*/};
  Double_t yl[21]={260, 360, 320, 300, 300, 250, 170, /*180,*/ 130, /*150,*/ 100,  /*120,*/  100,  /*120,  130,*/  100,  /*100,  100,*/  100,  /*0, 0*/};
  Double_t exl[21];
  Double_t eyl[21];

  TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
  gr1->SetMarkerColor(kBlue);
  gr1->SetMarkerStyle(21);

  //gr1->Draw("LP");

  TSpline3 *s = new TSpline3("grs",gr1);
  s->SetLineColor(kBlue);
  s->SetLineStyle(2);
  s->SetLineWidth(3);

  return gr1;
}

TGraphErrors* get1fbUp_LO(){

  Int_t nl = 21;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800,1900,2000};
  Double_t yl[21]={260, 410, 380, 360, 360, 360, 320, 240, 200, 170, 160 , 140,  140,  140,  120,  120,  110,  110,  110, 0, 0};
  Double_t exl[21];
  Double_t eyl[21];

  TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
  gr1->SetMarkerColor(kBlue);
  gr1->SetMarkerStyle(21);

  //gr1->Draw("LP");

  TSpline3 *s = new TSpline3("grs",gr1);
  s->SetLineColor(kBlue);
  s->SetLineStyle(2);
  s->SetLineWidth(3);

  return gr1;

}
TGraphErrors* get1fbLow_LO(){

  Int_t nl = 21;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900,2000};
  Double_t yl[21]={260, 340, 300, 300, 280, 230, 150, 110, 110, 110, 100,  90,  90,  80,   80,   80,   80,   80,   80,  0,   0};
  Double_t exl[21];
  Double_t eyl[21];

  TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
  gr1->SetMarkerColor(kBlue);
  gr1->SetMarkerStyle(21);

  //gr1->Draw("LP");

  TSpline3 *s = new TSpline3("grs",gr1);
  s->SetLineColor(kBlue);
  s->SetLineStyle(2);
  s->SetLineWidth(3);

  return gr1;

}

TGraphErrors* get1fbExp_LO(){

  Int_t nl = 21;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800,1900,2000};
  Double_t yl[21]={260, 380, 340, 320, 320, 300, 240, 200, 150, 120, 110,  100,  100,  100,  100,  100,  100,  100,  90, 0, 0};
  Double_t exl[21];
  Double_t eyl[21];

  TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
  gr1->SetMarkerColor(kBlue);
  gr1->SetMarkerStyle(21);

  //gr1->Draw("LP");

  TSpline3 *s = new TSpline3("grs",gr1);
  s->SetLineColor(kBlue);
  s->SetLineStyle(2);
  s->SetLineWidth(3);

  return gr1;

}


TGraphErrors* get1fbObs(){
  Int_t nl = 21-2;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, 700,  800,  900,  1000,  1100,  1200,  1300, 1400, 1500,  1600, 1700,  1800,  /*1900,2000*/};
  Double_t yl[21]={260, 420, 410, 400, 380, 370, 360, 320,  260,  220,  200,   190,   180,   170,  160,  160,   155,  150,   140,  /*0, 0*/};
  Double_t exl[21];
  Double_t eyl[21];

  TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
  gr1->SetMarkerColor(kBlue);
  gr1->SetMarkerStyle(21);

  //gr1->Draw("LP");

  TSpline3 *s = new TSpline3("grs",gr1);
  s->SetLineColor(kBlue);
  s->SetLineStyle(2);
  s->SetLineWidth(3);

  return gr1;
}

TGraphErrors* get1fbUp(){

  Int_t nl = 21-2;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800/*,1900,2000*/};
  Double_t yl[21]={260, 430, 420, 410, 390, 390, 370, 350, 300, 250, 230 , 220,  220,  220,  210,  200,  200,  190,  180/*, 0, 0*/};
  Double_t exl[21];
  Double_t eyl[21];

  TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
  gr1->SetMarkerColor(kBlue);
  gr1->SetMarkerStyle(21);

  //gr1->Draw("LP");

  TSpline3 *s = new TSpline3("grs",gr1);
  s->SetLineColor(kBlue);
  s->SetLineStyle(2);
  s->SetLineWidth(3);

  return gr1;

}
TGraphErrors* get1fbLow(){

  Int_t nl = 21-2;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800/*, 1900,2000*/};
  Double_t yl[21]={250, 380, 350, 340, 320, 300, 260, 240, 210, 150, 120,   120,   110,   110,   110,   100,   100,   100,   90/*,  0,   0*/};
  Double_t exl[21];
  Double_t eyl[21];

  TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
  gr1->SetMarkerColor(kBlue);
  gr1->SetMarkerStyle(21);

  //gr1->Draw("LP");

  TSpline3 *s = new TSpline3("grs",gr1);
  s->SetLineColor(kBlue);
  s->SetLineStyle(2);
  s->SetLineWidth(3);

  return gr1;

}


TGraphErrors* get1fbExp(){

  Int_t nl = 21-2;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800/*, 1900, 2000*/};
  Double_t yl[21]={260, 400, 380, 370, 360, 350, 340, 300, 260, 220, 190,  190,  180,  170,  160,  150,  140,  140,  130/*,  0,    0*/};
  Double_t exl[21];
  Double_t eyl[21];

  TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
  gr1->SetMarkerColor(kBlue);
  gr1->SetMarkerStyle(21);

  //gr1->Draw("LP");

  TSpline3 *s = new TSpline3("grs",gr1);
  s->SetLineColor(kBlue);
  s->SetLineStyle(2);
  s->SetLineWidth(3);

  return gr1;

}



TGraphErrors* getATLAScomb(){

  Int_t nl = 10;
  Double_t xl[10]={ 50,150,250,350,450,550,650,750,850,950};
  Double_t yl[10]={420,420,415,400,375,340,300,260,235,205};
  Double_t exl[10];
  Double_t eyl[10];

  TGraphErrors* gr1 = new TGraphErrors(nl,xl,yl,exl,eyl);
  gr1->SetMarkerColor(kBlue);
  gr1->SetMarkerStyle(21);

  //gr1->Draw("LP");

  TSpline3 *s = new TSpline3("grs",gr1);
  s->SetLineColor(kBlue);
  s->SetLineStyle(2);
  s->SetLineWidth(3);

  return gr1;

}





