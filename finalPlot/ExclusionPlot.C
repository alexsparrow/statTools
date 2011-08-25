#include <iostream>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <sstream>
#include <vector>
#include <string>

#include "ExclusionPlot.hh"

#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TCanvas.h"
#include "TMarker.h"
#include "vector.h"
#include "TMath.h"
#include "TList.h"
#include "TGraph.h"
#include "TObjArray.h"

void ExclusionPlot(){
  gStyle->SetPalette(1);

  Int_t tanBeta = 10;
  CommandMSUGRA("1100pb_expected.root",tanBeta,1);


}



void CommandMSUGRA(TString plotName_,
       Int_t tanBeta_){

  //convert tanb value to string
  std::stringstream tmp;
  tmp << tanBeta_;
  TString tanb( tmp.str() );

  lo = false;

  // Output file
  cout << " create " << plotName_ << endl;
  TFile* output = new TFile( plotName_, "RECREATE" );
  if ( !output || output->IsZombie() ) { std::cout << " zombie alarm output is a zombie " << std::endl; }


  //set old exclusion Limits
  // TGraph* LEP_ch = set_lep_ch(tanBeta_);
  // TGraph* myLEP_ch = set_lep_ch(tanBeta_);
  // myLEP_ch->SetFillColor(10);
  // myLEP_ch->SetFillStyle(1001);
  // TGraph* LEP_sl = set_lep_sl(tanBeta_);//slepton curve
  // TGraph* TEV_sg_cdf = set_tev_sg_cdf(tanBeta_);//squark gluino cdf
  // TGraph* TEV_sg_d0 = set_tev_sg_d0(tanBeta_);//squark gluino d0
  TGraph* stau = set_tev_stau(tanBeta_);//stau

  // TGraph* // TEV_sn_d0_1 = set_sneutrino_d0_1();
  // TGraph* // TEV_sn_d0_2 = set_sneutrino_d0_2();

  //constant ssqquark and gluino lines
  TF1* lnsq[10];
  TF1* lngl[10];

  TLatex* sq_text[10];
  TLatex* gl_text[10];

  for(int i = 1; i < 6; i++){
    lnsq[i] = constant_squark(tanBeta_,i);
    sq_text[i] = constant_squark_text(i,*lnsq[i],tanBeta_);
    lngl[i] = constant_gluino(i);
    gl_text[i] = constant_gluino_text(i,*lngl[i],tanBeta_);
  }

  //Legends
  TLegend* legst = makeStauLegend(0.05,tanBeta_);
  // TLegend* legexp = makeExpLegend( *TEV_sg_cdf,*TEV_sg_d0,*LEP_ch,*LEP_sl,*TEV_sn_d0_1,0.03,tanBeta_);


  //make Canvas
  TCanvas* cvsSys = makeCanvas(tanb);
  output->cd();

  //and now
  //the exclusion limits
  TGraphErrors* First ;
  TGraphErrors* Second;
  //  TGraphErrors* Third;
  TGraphErrors* Second_up;
  TGraphErrors* Second_low;
  TGraphErrors* LS_obs;
  TGraphErrors* LS_exp;
  TGraphErrors* LS_up;
  TGraphErrors* LS_low;

  // QCDZero = get776QCDZeroExp();
  // QCDSideBand = get776SidBandExp();
  if(tanBeta_ == 3){
    First = getObserved_NLO_tanBeta3();
    Second = getExpected_NLO_tanBeta3();
    Second_up = getExpected_NLO_tanBeta3_up();
    Second_low = getExpected_NLO_tanBeta3_low();
    //    Third = getLO_tanBeta3();
  }
  if(tanBeta_ == 10){

    if(lo){
      First = get1fbObs_LO();
      Second = get1fbExp_LO();
      Second_up = get1fbUp_LO();
      Second_low = get1fbLow_LO();
    }
    else{
      First = get1fbObs();
      Second = get1fbExp();
      Second_up = get1fbUp();
      Second_low = get1fbLow();
      LS_obs = get1fbObs_LS();
      LS_exp = get1fbExp_LS();
      LS_up = get1fbUp_LS();
      LS_low = get1fbLow_LS();
    }
  }
  if(tanBeta_ == 50){
    First = getObserved_NLO_tanBeta50();
    Second = getExpected_NLO_tanBeta50();
    Second_up = getExpected_NLO_tanBeta50_up();
    Second_low = getExpected_NLO_tanBeta50_low();
    //    Third = getLO_tanBeta50();
  }

  TGraphErrors* obs250;
  obs250 = get250Obs();

  TGraphErrors* ATLcomb;
  ATLcomb = getATLAScomb();

  double m0min = 0;
  if (tanBeta_ == 50) m0min=200;



  //   TH2F* hist = getHisto("/home/hep/elaird1/public_html/57_stat_plots/05_cmssm_fc/","ExclusionLimit","feldmanCousins_tanBeta"+tanb+"_nlo_1HtBin_expR.root");

  TH2F* hist = new TH2F("h1","h1",100,0, 1800, 100,80, 440);

  hist->GetXaxis()->SetRangeUser(0,2000);
  if (tanBeta_ == 10)  hist->GetXaxis()->SetRangeUser(0,2000);
  if (tanBeta_ == 50)  hist->GetXaxis()->SetRangeUser(0,2000);
  hist->GetYaxis()->SetRangeUser(80,450);


  hist->SetLineWidth(3);
  hist->SetLineColor(9);
  hist->SetLineStyle(2);

  output->cd();
  hist->Reset();
  hist->Draw();

  cvsSys->Update();

  hist->GetXaxis()->SetTitle("m_{0} (GeV)");
  hist->GetYaxis()->SetTitle("m_{1/2} (GeV)");
  hist->GetYaxis()->SetTitleOffset(1.);
  hist->GetXaxis()->SetNdivisions(506);
  //  if (tanBeta_ == 50)  hist->GetXaxis()->SetNdivisions(504);
  hist->GetYaxis()->SetNdivisions(506);



  int col[]={2,3,4};

  TSpline3 *sobs250 = new TSpline3("sobs250",obs250);
  sobs250->SetLineColor(kBlue);
  sobs250->SetLineWidth(3);

  TSpline3 *sobs250 = new TSpline3("sobs250",obs250);
  sobs250->SetLineColor(kBlue);
  sobs250->SetLineWidth(3);

  TSpline3 *sobs250 = new TSpline3("sobs250",obs250);
  sobs250->SetLineColor(kBlue);
  sobs250->SetLineWidth(3);

  TSpline3 *sobs250 = new TSpline3("sobs250",obs250);
  sobs250->SetLineColor(kBlue);
  sobs250->SetLineWidth(3);


  TSpline3 *sATLcomb = new TSpline3("sATLcomb",ATLcomb);
  sATLcomb->SetLineColor(kGreen);
  sATLcomb->SetLineWidth(3);


  TSpline3 *sFirst = new TSpline3("sFirst",First);
  sFirst->SetLineColor(kBlue);
  sFirst->SetLineWidth(3);

  TSpline3 *sSecond = new TSpline3("sSecond",Second);
  sSecond->SetLineColor(kCyan);
  sSecond->SetLineStyle(4);
  sSecond->SetLineWidth(2);

  TSpline3 *sSecond_up = new TSpline3("sSecond_up",Second_up);
  sSecond_up->SetLineColor(kCyan);
  sSecond_up->SetLineStyle(1);
  sSecond_up->SetLineWidth(2);

  TSpline3 *sSecond_low = new TSpline3("sSecond_low",Second_low);
  sSecond_low->SetLineColor(kCyan);
  sSecond_low->SetLineStyle(1);
  sSecond_low->SetLineWidth(2);

  TSpline3 *sLS_obs = new TSpline3("sLS_obs",LS_obs);
  sLS_obs->SetLineColor(kRed);//kGreen+2);
  sLS_obs->SetLineWidth(3);

  TSpline3 *sLS_exp = new TSpline3("sLS_exp",LS_exp);
  sLS_exp->SetLineColor(kRed-7);//kGreen);
  sLS_exp->SetLineStyle(4);
  sLS_exp->SetLineWidth(2);

  TSpline3 *sLS_up = new TSpline3("sLS_up",LS_up);
  sLS_up->SetLineColor(kRed-7);//kGreen);
  sLS_up->SetLineStyle(1);
  sLS_up->SetLineWidth(2);

  TSpline3 *sLS_low = new TSpline3("sLS_low",LS_low);
  sLS_low->SetLineColor(kRed-7);//kGreen);
  sLS_low->SetLineStyle(1);
  sLS_low->SetLineWidth(2);


  // TSpline3 * sThird = new TSpline3("sThird", Third);
  // sThird->SetLineColor(kOrange);
  // sThird->SetLineWidth(3);
  // TSpline3 *sQCDZero = new TSpline3("sQCDZero",QCDZero);
  // sQCDZero->SetLineColor(kPink-7);
  // sQCDZero->SetLineWidth(3);
  // TSpline3 *sQCDSideBand = new TSpline3("sQCDSideBand",QCDSideBand);
  // sQCDSideBand->SetLineColor(kBlue-7);
  // sQCDSideBand->SetLineWidth(3);

  //  TSpline3 *sThird = new TSpline3("sThird",Third);
  //  sThird->SetLineColor(kGreen+2);
  //  sThird->SetLineStyle(4);
  //  sThird->SetLineWidth(3);

  // UNCOMMENT!!!
  sSecond_up->Draw("same");
  sSecond_low->Draw("same");

  sLS_up->Draw("same");
  sLS_low->Draw("same");

  //  sThird->Draw("same");

  //constant squark and gluino mass contours
  for (int it=1;it<6;it++) {
    lngl[it]->Draw("same");
    lnsq[it]->Draw("same");
    // if(it != 5)
    if(it != 5) sq_text[it]->Draw();
    gl_text[it]->Draw();
  }


  //exclusion limits previous experiments
  if(tanBeta_ == 3){
    // TEV_sn_d0_1->Draw("fsame");
    // TEV_sn_d0_2->Draw("fsame");
  }
  // LEP_ch->Draw("fsame");
  // if (tanBeta_ != 50) LEP_sl->Draw("fsame");

  // TEV_sg_cdf->Draw("fsame");
  // TEV_sg_d0->Draw("same");
  // TEV_sg_d0->Draw("fsame");


  //other labels
  Double_t xpos = 0;
  Double_t xposi = 0;
  Double_t ypos = 0;
  if(tanBeta_ == 50) xposi = 150;
  if(tanBeta_ == 50) xpos = 200;
  if(tanBeta_ == 50) ypos = -10;

  TLatex* lumilabel = new TLatex(.15,0.937,"CMS     L_{int} = 1.1 fb^{-1}, #sqrt{s} = 7 TeV");
  lumilabel->SetNDC();
  lumilabel->SetTextSize(0.05);

  lumilabel->Draw("same");

  TString text_tanBeta;
  text_tanBeta =  "tan#beta = "+tanb+", A_{0} = 0, #mu > 0";
  TLatex* cmssmpars = new TLatex(1000.+xpos,450.+ypos,text_tanBeta);
  cmssmpars->SetTextSize(0.04);

  cmssmpars->Draw("same");

  //LM points
  TMarker* LM0 = new TMarker(200.,160.,20);
  TMarker* LM1 = new TMarker(60.,250.,20);

  LM0->SetMarkerSize(1.2);
  LM1->SetMarkerSize(1.2);

  TLatex* tLM0 = new TLatex(205.,160.,"LM0");
  tLM0->SetTextSize(0.035);

  TLatex* tLM1 = new TLatex(65.,243.,"LM1");
  tLM1->SetTextSize(0.035);

  if (tanBeta_ != 50){
    // LM0->Draw("same");
    // tLM0->Draw("same");
    // LM1->Draw("same");
    // tLM1->Draw("same");
  }



  //expected and observed (LO & NLO) contours
  TLegend* myleg = new TLegend(0.5,0.65,0.9,0.9,NULL,"brNDC");
  myleg->SetFillColor(0);
  myleg->SetShadowColor(0);
  myleg->SetTextSize(0.03);
  myleg->SetBorderSize(0);


  myleg->SetHeader("95% C.L. Limits:");
  //myleg->AddEntry(sFirst,"Observed Limit (NLO), PL","L");
  if(lo){
    myleg->AddEntry(sFirst,"Observed Limit (LO), CL_{s}","L");
  }
  else{
    myleg->AddEntry(sFirst,"L_{P}: Observed Limit (NLO), CL_{s}","L");
  }
  // myleg->AddEntry(sQCDZero,"#alpha_{T} shape analysis PL QCD(0), EWK flat (LO), 769pb^{-1} (Expected)","L");
  // myleg->AddEntry(sQCDSideBand,"#alpha_{T} shape analysis PL QCD(EXP) sideband, EWK flat (LO), 769pb^{-1} (expected)","L");
  // myleg->AddEntry(sATLcomb,"ATLAS: 0lep combined CLs (NLO), 165pb^{-1}","L");
  // myleg->AddEntry(,"#alpha_{T} cut&count, 35pb^{-1}","L");

  myleg->AddEntry(sSecond,"L_{P}: Median Expected Limit","L");
  myleg->AddEntry(sSecond_up,"L_{P}: Expected Limit #pm 1 #sigma","F");

  myleg->AddEntry(sLS_obs, "LS : Observed Limit (NLO), CL_{s}", "L");
  myleg->AddEntry(sLS_exp, "LS : Median Expected Limit", "L");
  myleg->AddEntry(sLS_up, "LS : Expected Limit #pm 1 #sigma", "F");

  sSecond_up->SetFillStyle(4010);
  sSecond_up->SetFillColor(kCyan-10);

  sSecond_low->SetFillStyle(1001);
  sSecond_low->SetFillColor(10);

  // sLS_up->SetFillStyle(4010);
  // sLS_up->SetFillColor(kGreen+2-10);

  // sLS_low->SetFillStyle(1001);
  // sLS_low->SetFillColor(10);

  sFirst->Draw("same");
  sLS_obs->Draw("same");

  // UNCOMMENT!!!!
  sSecond->Draw("same");
  sLS_exp->Draw("same");
  // sQCDZero->Draw("same");
  // sQCDSideBand->Draw("same");

  // sobs250->Draw("same");
  // sATLcomb->Draw("same");

  TLine* scan = new TLine(0,455,800,455);
  scan->SetLineColor(1);
  scan->SetLineWidth(15);
  // scan->Draw("same");
  TLatex* scanlabel = new TLatex(100,470,"End of CMS scan");
  scanlabel->SetTextSize(0.04);
  // scanlabel->Draw("same");

  //stau=LSP contour
  stau->Draw("fsame");

  //legends
  // legexp->Draw();
  legst->Draw();
  myleg->Draw();

  if(tanBeta_ == 50){
    // myLEP_ch->Draw("fsame");
    // LEP_ch->Draw("fsame");

    // TEV_sg_cdf->Draw("fsame");
    // TEV_sg_d0->Draw("same");
    // TEV_sg_d0->Draw("fsame");
  }

  hist->Draw("sameaxis");
  cvsSys->RedrawAxis();

  cvsSys->Update();

  cvsSys->Write();


  cvsSys->SaveAs("RA4_ExclusionLimit_tanb"+tanb+".pdf");
  cvsSys->SaveAs("RA4_ExclusionLimit_tanb"+tanb+".png");


  output->Write();
  output->Close();
  delete output;

}


