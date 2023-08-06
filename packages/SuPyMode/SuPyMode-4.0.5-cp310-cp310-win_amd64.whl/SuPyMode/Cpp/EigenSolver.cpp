#pragma once

#include "Extrapolate.hpp"
#include "Laplacian.cpp"
#include "SuperMode.cpp"
#include "Definitions.cpp"
#include "Utils.cpp"
#include "Wrapper.cpp"

class CppSolver : public BaseLaplacian
{
  public:
    size_t             nComputedMode, nSortedMode, MaxIter, DegenerateFactor, ITRLength, Order, ExtrapolOrder;
    ScalarType         Tolerance, k, kInit, kDual, lambda, MaxIndex;
    ScalarType        *MeshPtr, *ITRPtr;
    std::vector<double> ITRList;
    MSparse            EigenMatrix, Identity, M;
    VectorType         MeshGradient;
    Eigen::BiCGSTAB<MSparse>  Solver;
    std::vector<SuperMode> SuperModes, SortedSuperModes;
    

  CppSolver(ndarray    &Mesh,
            ndarray    &PyMeshGradient,
            Vecf2D     &FinitDiffMatrix,
            size_t     nComputedMode,
            size_t     nSortedMode,
            size_t     MaxIter,
            ScalarType Tolerance,
            ScalarType dx,
            ScalarType dy,
            ScalarType Wavelength,
            bool       Debug
            )
               : BaseLaplacian(Mesh, dx, dy)
                {
                 this->FinitDiffMatrix   = FinitDiffMatrix;
                 this->Debug             = Debug;
                 this->nComputedMode             = nComputedMode;
                 this->nSortedMode             = nSortedMode;
                 this->MaxIter           = MaxIter;
                 this->Tolerance         = Tolerance;

                 this->MeshPtr           = (ScalarType*) Mesh.request().ptr;
                 this->lambda            = Wavelength;
                 this->k                 = 2.0 * PI / Wavelength;
                 this->kInit             = this->k;
                 ScalarType *adress      = (ScalarType*) PyMeshGradient.request().ptr;

                 Eigen::Map<VectorType> MeshGradient( adress, size );
                 this->MeshGradient = MeshGradient;

                 GenerateModeSet();

                 ComputeMaxIndex();
               }


   SuperMode GetMode(size_t Mode){ return SortedSuperModes[Mode]; }

   void SwapMode(SuperMode &Mode0, SuperMode &Mode1);


  void SetSymmetries(int LeftSymmetry, int RightSymmetry, int TopSymmetry, int BottomSymmetry)
  {
      this->LeftSymmetry = LeftSymmetry;
      this->RightSymmetry = RightSymmetry;
      this->TopSymmetry = TopSymmetry;
      this->BottomSymmetry = BottomSymmetry;
  }

   void GenerateModeSet()
   {
     for (int i=0; i<nComputedMode; ++i)
        SuperModes.push_back(SuperMode(i));

     for (int i=0; i<nSortedMode; ++i)
        SortedSuperModes.push_back(SuperMode(i));

   }

   MSparse ComputeMatrix()
   {
       EigenMatrix = BaseLaplacian::Laplacian;

       size_t iter = 0;

       for(size_t i=0; i<Nx; ++i)
          for(size_t j=0; j<Ny; ++j){
              Identity.coeffRef(iter,iter) = + pow( MeshPtr[iter] * kDual, 2);
              ++iter;
            }

       EigenMatrix += Identity;

       Identity.setIdentity();

       return -1.0*EigenMatrix;
       }


   tuple<MatrixType, VectorType> ComputeEigen(ScalarType alpha){

       MSparse EigenMatrix = ComputeMatrix();

       Spectra::SparseGenRealShiftSolve<ScalarType> op(EigenMatrix);

       Spectra::GenEigsRealShiftSolver<Spectra::SparseGenRealShiftSolve<ScalarType>> eigs(op, nComputedMode, 2*nComputedMode, alpha);

       eigs.init();

       int nconv = eigs.compute(Spectra::SortRule::LargestMagn, MaxIter, Tolerance);

       MatrixType Vectors = eigs.eigenvectors().real();

       VectorType Values = eigs.eigenvalues().real();

       return std::make_tuple(Vectors, Values);
       }


   void ComputeLaplacian(){
     
     Identity = MSparse(size,size); Identity.setIdentity();

     FromTriplets();
   }


   void PrepareSuperModes()
   {
     for (SuperMode& mode : SuperModes)
         mode.Init(ITRLength, Nx, Ny, LeftSymmetry, RightSymmetry, TopSymmetry, BottomSymmetry, nSortedMode);
   }


   void PopulateModes(size_t Slice, MatrixType& EigenVectors, VectorType& EigenValues)
   {
     for (SuperMode& mode : SuperModes)
     {
       mode.Fields.col(Slice)   << EigenVectors.col(mode.ModeNumber);
       mode.Fields.col(Slice).normalize();
       mode.Betas[Slice]        = sqrt( - EigenValues[mode.ModeNumber] ) / ITRList[Slice];
       mode.EigenValues[Slice]  = EigenValues[mode.ModeNumber];
       mode.Index[Slice]        = sqrt( abs( mode.EigenValues[Slice] ) ) / (ITRList[Slice] * kInit);
     }

   }


   void LoopOverITR(std::vector<double> ITRList, size_t order = 1, ScalarType alpha=0){
     this->ITRList     = ITRList;

     ITRLength        = ITRList.size();


     kInit            = 2.0 * PI / lambda;

     MatrixType EigenVectors;
     VectorType EigenValues;

     PrepareSuperModes();


     std::vector<ScalarType> AllFirstEigenValues;
     AllFirstEigenValues.reserve(ITRLength);

     if (alpha == 0)
        alpha = -pow( k * ComputeMaxIndex(), 2 );



     for (size_t slice=0; slice<ITRLength; ++slice)
     {

       if (Debug)
       {
         size_t barWidth = 70;
         std::cout << "[";

         double progress = (double) slice/ITRLength;

         size_t pos = (size_t) (barWidth * progress);

         for (size_t i = 0; i < barWidth; ++i) {
             if (i < pos) std::cout << "=";
             else if (i == pos) std::cout << ">";
             else std::cout << " ";
         }
         std::cout << "] " << "ITR: " <<ITRList[slice] << "\n";
         std::cout.flush();

       }

       kDual = kInit * ITRList[slice];

       tie(EigenVectors, EigenValues) = ComputeEigen(alpha);

       PopulateModes(slice, EigenVectors, EigenValues);

       AllFirstEigenValues.push_back(EigenValues[0]);

       size_t next = slice+1, mode=0;

       alpha = ExtrapolateNext(order, AllFirstEigenValues, ITRList, next);
     }

   }

    vector<size_t> ComputecOverlaps(size_t Slice)
    {

        ScalarType BestOverlap, Overlap;
        vector<size_t> Indices(nSortedMode);

        for (size_t i=0; i<nSortedMode; ++i)
        {
        BestOverlap = 0;
        for (size_t j=0; j<nComputedMode; ++j)
        {
            SuperMode Mode0 = SuperModes[i], Mode1 = SuperModes[j];

            Overlap = Mode0.ComputeOverlap(Mode1, Slice);

            if (Overlap > BestOverlap) {Indices[i] = j; BestOverlap = Overlap;}
        }
        if (BestOverlap<0.8)
        std::cout<<"Bad mode correspondence: "<< BestOverlap <<"  At ITR: "<< ITRList[Slice] <<". You should consider makes more ITR steps"<<std::endl;
        }

    return Indices;

    }




    void SortModes(std::string Type)
    {
        std::cout<<"Sorting SuperModes\n";

        for (SuperMode &mode : SortedSuperModes)
        {
            mode.Init(ITRLength, Nx, Ny, LeftSymmetry, RightSymmetry, TopSymmetry, BottomSymmetry, nSortedMode);
        }

        if (Type == "field") SortModesFields();
        else if (Type == "index") SortModesIndex();
        else if (Type == "none") SortModesNone();

    }

    void SortSliceIndex(size_t Slice)
    {
        vector<ScalarType> Betas;
        Betas.reserve(nComputedMode);

        size_t iter=0;
        for (size_t mode=0; mode<nSortedMode; ++mode)
        {
            Betas.push_back(SuperModes[mode].Betas[Slice]);

            ++iter;
        }

        vector<size_t> sorted = sort_indexes( Betas );

        for (size_t mode=0; mode<nSortedMode; ++mode)
        {
            auto order = sorted[mode];
            SortedSuperModes[mode].CopyOtherSlice(SuperModes[order], Slice);
        }
    }


    void SortModesIndex()
    {
        for (size_t l=0; l<ITRLength; ++l)
            SortSliceIndex(l);
    }


    void SortModesFields()
    {
        for (size_t mode=0; mode<nSortedMode; ++mode)
            SortedSuperModes[mode] = SuperModes[mode];

        for (size_t slice=0; slice<ITRLength-1; ++slice)
            SortSliceFields(slice);
    }


    std::vector<std::vector<size_t>> Get_Max_Index(Eigen::MatrixXf &Matrix)
    {
        std::vector<std::vector<size_t>> MaxIndex;
        Eigen::MatrixXf::Index max_index;

        for (size_t row=0; row < nSortedMode; row++ )
        {
            Matrix.row(row).maxCoeff(&max_index);
            MaxIndex.push_back( {row, (size_t) max_index} );
            Matrix.col(max_index) *= 0.;
        }
        return MaxIndex;
    }


    void SortSliceFields(size_t &Slice)
    {
        Eigen::MatrixXf Overlap_matrix = GetOverlapMatrix(Slice);

        std::vector<std::vector<size_t>> MaxIndex = Get_Max_Index(Overlap_matrix);
        

        for (auto couple: MaxIndex)
        {
            SuperMode &Mode0 = SortedSuperModes[couple[0]],
                      &Mode1 = SuperModes[couple[1]];

            Mode0.Fields.col(Slice+1) = Mode1.Fields.col(Slice+1);
            Mode0.Betas[Slice+1]      = Mode1.Betas[Slice+1];
            Mode0.Index[Slice+1]      = Mode1.Index[Slice+1];
        }
    }

    Eigen::MatrixXf GetOverlapMatrix(size_t &Slice)
    {
        Eigen::MatrixXf Matrix(nSortedMode, nComputedMode);

        for (SuperMode &Mode0 : SortedSuperModes)
            for (SuperMode &Mode1 : SuperModes)
                Matrix(Mode0.ModeNumber, Mode1.ModeNumber) = abs( Mode0.ComputeOverlap(Mode1, Slice, Slice+1) );

        return Matrix;

    }

    void SwapModes(SuperMode &Mode0, SuperMode &Mode1, size_t &&Slice)
    {
        Mode0.Fields.col(Slice) = Mode1.Fields.col(Slice);
        Mode0.Betas[Slice]      = Mode1.Betas[Slice];
        Mode0.Index[Slice]      = Mode1.Index[Slice];
    }


    void _SortSliceFields(size_t Slice)
    {
        for (size_t previous=0; previous<nSortedMode; ++previous)
        {
            SuperMode &Mode0 = SortedSuperModes[previous];
            std::vector<ScalarType> Overlaps(nComputedMode, 0);

            for (size_t after=0; after<nComputedMode; ++after)
                {
                    SuperMode &Mode1 = SuperModes[after];
                    Overlaps[after] = abs( Mode0.Fields.col(Slice).transpose() * Mode1.Fields.col(Slice+1)  );
                }


            size_t bestFit = GetMaxValueIndex(Overlaps);

            SwapModes(Mode0, SuperModes[bestFit], Slice+1);
        }
   }



    void SortModesNone()
    {
        for (size_t mode=0; mode<nSortedMode; ++mode)
             SortedSuperModes[mode] = SuperModes[mode];
    }

















   void ComputeCoupling()
   {

     std::cout<<"Computing coupling\n";

     for (size_t slice=0; slice<ITRLength; ++slice)
         for (SuperMode &mode0 : SortedSuperModes)
             for (size_t m=0; m<nSortedMode;++m)
                 {
                   SuperMode &mode1 = SortedSuperModes[m];

                   mode1.ComputeCoupling(mode0, slice, MeshGradient, kInit);

                 }

   }


   void ComputeAdiabatic(){

     std::cout<<"Computing adiabatic\n";

     for (size_t slice=0; slice<ITRLength; ++slice)
         for (SuperMode &mode0 : SortedSuperModes)
             for (size_t m=0; m<nSortedMode;++m)
                 {
                   SuperMode &mode1 = SortedSuperModes[m];
                   mode1.Adiabatic(mode0.ModeNumber, slice) = mode1.ComputeAdiabatic(mode0, slice, MeshGradient, kInit);
                 }

   }


   void ComputeCouplingAdiabatic()
   {
     std::cout<<"Computing coupling/adiabatic\n";

     for (size_t slice=0; slice<ITRLength; ++slice)
         for (SuperMode &mode0 : SortedSuperModes)
             for (size_t m=0; m<nSortedMode;++m)
               mode0.PopulateCouplingAdiabatic(SortedSuperModes[m], slice, MeshGradient, kInit);
   }

   ScalarType ComputeMaxIndex()
   {
     MaxIndex = 0.0;
     for (size_t i=0; i<size; ++i)
        if (MeshPtr[i] > MaxIndex)
            MaxIndex = MeshPtr[i];

    return MaxIndex;
   }


   tuple<ndarray, ndarray> GetSlice(size_t Slice)
   {
     MatrixType OutputFields(size, nSortedMode);
     VectorType OutputBetas(nSortedMode);

     for (size_t mode=0; mode<nSortedMode; ++mode)
     {
       OutputFields.col(mode) = SuperModes[mode].Fields.col(Slice);
       OutputBetas[mode]      = SuperModes[mode].Betas[Slice];
     }

     ndarray FieldsPython = Eigen2ndarray_( OutputFields, { nSortedMode, Nx, Ny } ) ;

     ndarray BetasPython = Eigen2ndarray_( OutputBetas, { nSortedMode } ) ;

     return std::make_tuple( FieldsPython, BetasPython );
   }

};




PYBIND11_MODULE(CppSolver, module)
{
    pybind11::class_<CppSolver>(module, "CppSolver")
    .def(pybind11::init<ndarray&, ndarray&, Vecf2D&, size_t, size_t, size_t, ScalarType, ScalarType, ScalarType, ScalarType, bool>(),
         pybind11::arg("Mesh"),
         pybind11::arg("Gradient"),
         pybind11::arg("FinitMatrix"),
         pybind11::arg("nComputedMode"),
         pybind11::arg("nSortedMode"),
         pybind11::arg("MaxIter"),
         pybind11::arg("Tolerance"),
         pybind11::arg("dx"),
         pybind11::arg("dy"),
         pybind11::arg("Wavelength"),
         pybind11::arg("Debug") = false
       )

     .def("LoopOverITR",                 &CppSolver::LoopOverITR, pybind11::arg("ITR"), pybind11::arg("ExtrapolationOrder"), pybind11::arg("Alpha"))
     .def("ComputeAdiabatic",            &CppSolver::ComputeAdiabatic)
     .def("ComputeCouplingAdiabatic",    &CppSolver::ComputeCouplingAdiabatic)
     .def("ComputeCoupling",             &CppSolver::ComputeCoupling)
     .def("SortModes",                   &CppSolver::SortModes, pybind11::arg("Sorting"))
     .def("ComputeLaplacian",            &CppSolver::ComputeLaplacian)
     .def("GetSlice",                    &CppSolver::GetSlice, pybind11::arg("slice"))
     .def("GetMode",                     &CppSolver::GetMode)
     .def("SetSymmetries",               &CppSolver::SetSymmetries,  pybind11::arg("Left"),  pybind11::arg("Right"),  pybind11::arg("Top") , pybind11::arg("Bottom"))


     .def_readwrite("LeftSymmetry",   &CppSolver::LeftSymmetry)
     .def_readwrite("RightSymmetry",  &CppSolver::RightSymmetry)
     .def_readwrite("TopSymmetry",    &CppSolver::TopSymmetry)
     .def_readwrite("BottomSymmetry", &CppSolver::BottomSymmetry)
     .def_readwrite("nSortedMode",    &CppSolver::nSortedMode)
     .def_readwrite("nComputedMode",  &CppSolver::nComputedMode)
     .def_readwrite("ITRLength",      &CppSolver::ITRLength)
     .def_readwrite("ITRList",        &CppSolver::ITRList)
     .def_readwrite("Wavelength",     &CppSolver::lambda);
}

