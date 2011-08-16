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

TGraphErrors* get1fbObs(){

  Int_t nl = 21;
  Double_t xl[21]={0,   100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000};
  Double_t yl[21]={260, 400, 360, 320, 340, 360, 240, 180, 170, 140, 140,  140,  120,  120,  140,  120,  100,  100,  100,  80,   0};
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

  Int_t nl = 21;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800,1900,2000};
  Double_t yl[21]={260, 430, 420, 400, 400, 400, 380, 300, 300, 240, 200 , 180,  200,  180,  180,  200,  200,  180,  180, 0, 0};
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

  Int_t nl = 21;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900,2000};
  Double_t yl[21]={260, 380, 340, 320, 320, 340, 240, 180, 180, 150, 140,  120,  120,  120,  120,  120,  100,  100,  120,  0,   0};
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

  Int_t nl = 21;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800,1900,2000};
  Double_t yl[21]={260, 420, 380, 360, 380, 380, 280, 200, 220, 160, 160,  160,  120,  120,  120,  160,  140,  100,  170, 0, 0};
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

TGraphErrors* getCLS(){
  Int_t nl = 21-10;
  Double_t xl[21]={0  , 100, 200, 300, 400, 500, 600, /*700,*/ 800, /*900,*/ 1000, /*1100,*/ 1200, /*1300, 1400,*/ 1500, /*1600, 1700,*/ 1800, /*1900,2000*/};
  Double_t yl[21]={260, 400, 380, 350, 345, 340, 230, /*180,*/ 160, /*150,*/ 140,  /*120,*/  130,  /*120,  130,*/  125,  /*100,  100,*/  120,  /*0, 0*/};
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





