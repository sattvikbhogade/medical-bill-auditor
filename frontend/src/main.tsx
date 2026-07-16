import React from 'react'
import ReactDOM from 'react-dom/client'
import 'bootstrap/dist/css/bootstrap.min.css'
import './styles.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card shadow-sm border-0">
            <div className="card-body p-5">
              <h1 className="display-6 fw-semibold">Medical Bill Auditor</h1>
              <p className="lead text-muted mt-3">
                A clean, production-ready scaffold for the next phase of this platform.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </React.StrictMode>,
)
