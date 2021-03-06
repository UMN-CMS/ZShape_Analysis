#include "BackgroundFunctions.h"

#include <TMath.h>  // Erfc, Exp

double bg::analyticBackground(const double *x, const double *par){
    /*
     * par[0] = alpha
     * par[1] = beta
     * par[2] = gamma
     * par[3] = delta
     */
    const double erfout = TMath::Erfc((par[0] - x[0]) / par[3]);
    const double expout = TMath::Exp(-par[2] * x[0]);
    return par[1] * erfout * expout;
}

/*
 * BinnedBackground Class
 */
bg::BinnedBackground::BinnedBackground(TH1D * bgHisto){
    // Set up the internal histogram
    backgroundHisto_ = (TH1D*)bgHisto->Clone("bghisto");
    // Set up the internal function
    internalFunc_ = new TF1("basefunc", bg::analyticBackground, minMZ_, maxMZ_, nparams_);
}

void bg::BinnedBackground::fillBackgroundHisto_(const double* par){
    /*
     * Loop over each bin of the internal histogram, and integrate from the low
     * edge to the high edge
     */
    for (int i = 1; i <= backgroundHisto_->GetNbinsX(); ++i){
        // Find bin edges
        const double xlow = backgroundHisto_->GetBinLowEdge(i);
        const double xhigh = xlow + backgroundHisto_->GetBinWidth(i);
        // Intergrate over the bin
        const double binval = internalFunc_->Integral(xlow, xhigh, par);  //
        // Set bin
        backgroundHisto_->SetBinContent(i, binval);
    }
}

TH1D* bg::BinnedBackground::getBackgroundHisto(){
    return backgroundHisto_;
}

double bg::BinnedBackground::operator() (const double *x, const double *par){
    // Update the historgram with the new values from the fitter
    fillBackgroundHisto_(par);
    return backgroundHisto_->GetBinContent(backgroundHisto_->FindBin(x[0]));
}

/*
 * BinnedBackgroundAndSignal Class
 */

bg::BinnedBackgroundAndSignal::BinnedBackgroundAndSignal(TH1D* signalHisto){
    // Set up the internal histograms
    signalHisto_ = signalHisto;
    backgroundHisto_ = (TH1D*)signalHisto->Clone("bghisto");
    // Set up the internal function
    internalFunc_ = new TF1("basefunc", bg::analyticBackground, minMZ_, maxMZ_, nparams_);
    // Normalize the signal
    const double area = signalHisto_->Integral();
    signalHisto_->Scale(1. / area);
}

TH1D* bg::BinnedBackgroundAndSignal::getSignalHisto(){
    return signalHisto_;
}

double bg::BinnedBackgroundAndSignal::operator() (const double *x, const double *par){
    // Update the historgram with the new values from the fitter
    fillBackgroundHisto_(par);
    const double bg = backgroundHisto_->GetBinContent(backgroundHisto_->FindBin(x[0]));
    const double sg = par[4] * signalHisto_->GetBinContent(signalHisto_->FindBin(x[0]));
    return bg + sg;
}

/*
 * BinnedBackgroundAndSmearedSignal Class
 */

bg::BinnedBackgroundAndSmearedSignal::BinnedBackgroundAndSmearedSignal(TH1D* signalHisto, std::vector<double>* masses){
    // Set up the internal histograms
    signalHisto_ = signalHisto;
    signalMutableHisto_ = (TH1D*)signalHisto->Clone("mutablehisto");
    backgroundHisto_ = (TH1D*)signalHisto->Clone("bghisto");
    // Set up the internal function
    internalFunc_ = new TF1("basefunc", bg::analyticBackground, minMZ_, maxMZ_, nparams_);
    // Normalize the signal
    const double area = signalHisto_->Integral();
    signalHisto_->Scale(1. / area);
    // Set up masses
    masses_ = masses;
}

void bg::BinnedBackgroundAndSmearedSignal::smearSignalHisto_(const double mean, const double sigma) {
    // Zero out the histogram
    for (int i = 1; i <= signalMutableHisto_->GetNbinsX(); ++i){
        signalMutableHisto_->SetBinContent(i, 0.);
    }
    // Start the randomizer with fixed seed for reproducibility
    trand_ = new TRandom3(123456);
    // Run over the vector and smear it
    for (std::vector<double>::const_iterator i = masses_->begin(); i != masses_->end(); ++i) {
        const double new_mz = (*i) * trand_->Gaus(mean, sigma);
        signalMutableHisto_->Fill(new_mz);
    }
    // Normalize the signal
    const double area = signalMutableHisto_->Integral();
    signalMutableHisto_->Scale(1. / area);
}

TH1D* bg::BinnedBackgroundAndSmearedSignal::getSignalHisto(){
    return signalMutableHisto_;
}

double bg::BinnedBackgroundAndSmearedSignal::operator() (const double *x, const double *par){
    // Update the historgram with the new values from the fitter
    fillBackgroundHisto_(par);
    smearSignalHisto_(par[5], par[6]);
    const double bg = backgroundHisto_->GetBinContent(backgroundHisto_->FindBin(x[0]));
    const double sg = par[4] * signalMutableHisto_->GetBinContent(signalMutableHisto_->FindBin(x[0]));
    return bg + sg;
}
