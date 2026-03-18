from flask import Flask, request, jsonify, session, redirect
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

data_store = []

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Samanvya Foundation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            position: relative;
        }

        /* Admin Button in Top Corner */
        .admin-corner-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 100;
        }

        .admin-corner-btn button {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3);
            padding: 12px 30px;
            border-radius: 50px;
            color: white;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .admin-corner-btn button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }

        .admin-corner-btn button i {
            font-size: 18px;
        }

        /* Main Container */
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 80px 20px 40px 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .form-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 100%;
            animation: slideUp 0.5s ease;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Header Section */
        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header i {
            font-size: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
        }

        .header h1 {
            color: #333;
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .header h2 {
            color: #666;
            font-size: 18px;
            font-weight: 400;
        }

        /* Form Styles */
        .form-group {
            margin-bottom: 20px;
        }

        .input-icon {
            position: relative;
        }

        .input-icon i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #999;
            font-size: 16px;
            z-index: 1;
        }

        input, select {
            width: 100%;
            padding: 15px 15px 15px 45px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s ease;
            background: white;
            appearance: none;
        }

        select {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23999' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 15px center;
            background-size: 16px;
        }

        input:focus, select:focus {
            border-color: #667eea;
            outline: none;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
            font-size: 14px;
        }

        /* Row Layout for two columns */
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        /* Submit Button */
        .submit-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 16px 30px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        .submit-btn i {
            font-size: 18px;
        }

        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
            z-index: 1000;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .modal-content {
            background: white;
            padding: 40px;
            border-radius: 20px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 90%;
            max-width: 400px;
            text-align: center;
            animation: scaleIn 0.3s ease;
        }

        @keyframes scaleIn {
            from {
                transform: translate(-50%, -50%) scale(0.9);
                opacity: 0;
            }
            to {
                transform: translate(-50%, -50%) scale(1);
                opacity: 1;
            }
        }

        .modal-content i {
            font-size: 70px;
            color: #28a745;
            margin-bottom: 20px;
        }

        .modal-content h3 {
            color: #333;
            font-size: 24px;
            margin-bottom: 10px;
        }

        .modal-content p {
            color: #666;
            margin-bottom: 20px;
            line-height: 1.6;
        }

        .modal-content button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 40px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .modal-content button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        /* Responsive Design */
        @media (max-width: 600px) {
            .form-row {
                grid-template-columns: 1fr;
                gap: 0;
            }
            
            .form-card {
                padding: 30px 20px;
            }
            
            .header h1 {
                font-size: 28px;
            }
            
            .admin-corner-btn button {
                padding: 8px 20px;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <!-- Admin Button in Top Corner -->
    <div class="admin-corner-btn">
        <button onclick="window.location='/admin'">
            <i class="fas fa-lock"></i>
            Admin Login
        </button>
    </div>

    <!-- Main Container -->
    <div class="container">
        <div class="form-card">
            <div class="header">
                <i class="fas fa-hands-helping"></i>
                <h1>Samanvya Foundation</h1>
                <h2>Fill Form for Interested Course</h2>
            </div>

            <form id="form">
                <div class="form-row">
                    <div class="form-group">
                        <label>Full Name</label>
                        <div class="input-icon">
                            <i class="fas fa-user"></i>
                            <input type="text" name="name" placeholder="Enter your full name" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Age</label>
                        <div class="input-icon">
                            <i class="fas fa-calendar"></i>
                            <input type="number" name="age" placeholder="Enter your age" required>
                        </div>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label>Gender</label>
                        <div class="input-icon">
                            <i class="fas fa-venus-mars"></i>
                            <select name="gender" required>
                                <option value="">Select Gender</option>
                                <option>Male</option>
                                <option>Female</option>
                                <option>Other</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Qualification</label>
                        <div class="input-icon">
                            <i class="fas fa-graduation-cap"></i>
                            <select name="qualification" required>
                                <option value="">Highest Qualification</option>
                                <option>10th</option>
                                <option>12th</option>
                                <option>B.sc</option>
                                <option>B.com</option>
                                <option>B.A</option>
                                <option>Masters</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label>Interested Course</label>
                    <div class="input-icon">
                        <i class="fas fa-book-open"></i>
                        <select name="course" required>
                            <option value="">Select Course</option>
                            <option>MLT (Medical Lab Technology)</option>
                            <option>GRD (General Radiology & Diagnosis)</option>
                        </select>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label>Mobile Number</label>
                        <div class="input-icon">
                            <i class="fas fa-phone"></i>
                            <input type="text" name="mobile" placeholder="Enter 10 digit number" pattern="[0-9]{10}" maxlength="10" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Email Address</label>
                        <div class="input-icon">
                            <i class="fas fa-envelope"></i>
                            <input type="email" name="email" placeholder="Enter your email" required>
                        </div>
                    </div>
                </div>

                <button type="submit" class="submit-btn">
                    <i class="fas fa-paper-plane"></i>
                    Submit Application
                </button>
            </form>
        </div>
    </div>

    <!-- Thank You Modal -->
    <div class="modal" id="modal">
        <div class="modal-content">
            <i class="fas fa-check-circle"></i>
            <h3>Thank You!</h3>
            <p>Thank you for showing interest in our courses.<br>Our team will contact you soon.</p>
            <button onclick="closeModal()">Close</button>
        </div>
    </div>

    <script>
        document.getElementById("form").onsubmit = async function(e){
            e.preventDefault();

            let formData = new FormData(this);

            // Show loading state
            let submitBtn = this.querySelector('button[type="submit"]');
            let originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
            submitBtn.disabled = true;

            try {
                let res = await fetch("/submit", {
                    method: "POST",
                    body: formData
                });

                if(res.ok){
                    document.getElementById("modal").style.display = "block";
                    this.reset();
                }
            } catch (error) {
                alert("Something went wrong. Please try again.");
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        }

        function closeModal(){
            document.getElementById("modal").style.display = "none";
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            let modal = document.getElementById("modal");
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        // Mobile number validation
        document.querySelector('input[name="mobile"]').addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);
        });
    </script>
</body>
</html>
"""

@app.route("/submit", methods=["POST"])
def submit():
    data_store.append({
        "name": request.form["name"],
        "age": request.form["age"],
        "gender": request.form["gender"],
        "qualification": request.form["qualification"],
        "course": request.form["course"],
        "mobile": request.form["mobile"],
        "email": request.form["email"],
        "date": datetime.now().date()
    })
    return "OK"

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/dashboard")

    return """
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .login-container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                width: 90%;
                max-width: 400px;
                animation: slideUp 0.5s ease;
            }
            
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .login-header {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .login-header i {
                font-size: 50px;
                color: #667eea;
                margin-bottom: 15px;
            }
            
            .login-header h2 {
                color: #333;
                font-size: 24px;
            }
            
            .input-group {
                margin-bottom: 20px;
                position: relative;
            }
            
            .input-group i {
                position: absolute;
                left: 15px;
                top: 50%;
                transform: translateY(-50%);
                color: #999;
            }
            
            .input-group input {
                width: 100%;
                padding: 15px 15px 15px 45px;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                font-family: 'Poppins', sans-serif;
                font-size: 14px;
                transition: all 0.3s ease;
            }
            
            .input-group input:focus {
                border-color: #667eea;
                outline: none;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .login-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px;
                border-radius: 12px;
                width: 100%;
                font-family: 'Poppins', sans-serif;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }
            
            .login-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            
            .back-link {
                text-align: center;
                margin-top: 20px;
            }
            
            .back-link a {
                color: #666;
                text-decoration: none;
                font-size: 14px;
                transition: color 0.3s ease;
            }
            
            .back-link a:hover {
                color: #667eea;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="login-header">
                <i class="fas fa-user-shield"></i>
                <h2>Admin Login</h2>
            </div>
            
            <form method="post">
                <div class="input-group">
                    <i class="fas fa-user"></i>
                    <input type="text" name="username" placeholder="Username" required>
                </div>
                
                <div class="input-group">
                    <i class="fas fa-lock"></i>
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                
                <button type="submit" class="login-btn">
                    <i class="fas fa-sign-in-alt"></i>
                    Login
                </button>
            </form>
            
            <div class="back-link">
                <a href="/"><i class="fas fa-arrow-left"></i> Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin")

    today = datetime.now().date()
    today_count = len([d for d in data_store if d["date"] == today])
    
    # Calculate course-wise distribution
    mlt_count = len([d for d in data_store if d["course"] == "MLT" or d["course"] == "MLT (Medical Lab Technology)"])
    grd_count = len([d for d in data_store if d["course"] == "GRD" or d["course"] == "GRD (General Radiology & Diagnosis)"])

    rows = ""
    for i, d in enumerate(data_store, 1):
        rows += f"""
        <tr style="background-color: {'#f8f9fa' if i % 2 == 0 else 'white'};">
            <td>{i}</td>
            <td><strong>{d['name']}</strong></td>
            <td>{d['course'][:20] + '...' if len(d['course']) > 20 else d['course']}</td>
            <td>{d['mobile']}</td>
            <td>{d['email']}</td>
            <td>{d['date']}</td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Poppins', sans-serif;
                background: #f5f5f5;
                padding: 20px;
            }}
            
            .dashboard {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 20px;
                margin-bottom: 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 20px;
            }}
            
            .header h1 {{
                font-size: 28px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .header h1 i {{
                font-size: 35px;
            }}
            
            .logout-btn {{
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid white;
                padding: 10px 25px;
                border-radius: 12px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 10px;
                text-decoration: none;
            }}
            
            .logout-btn:hover {{
                background: white;
                color: #667eea;
            }}
            
            .stats-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .stat-card {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
                display: flex;
                align-items: center;
                gap: 20px;
                transition: transform 0.3s ease;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }}
            
            .stat-icon {{
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .stat-icon i {{
                font-size: 30px;
                color: white;
            }}
            
            .stat-info h3 {{
                color: #666;
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 5px;
            }}
            
            .stat-info p {{
                color: #333;
                font-size: 28px;
                font-weight: 700;
            }}
            
            .table-container {{
                background: white;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
                overflow-x: auto;
            }}
            
            .table-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                flex-wrap: wrap;
                gap: 15px;
            }}
            
            .table-header h2 {{
                color: #333;
                font-size: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .total-count {{
                background: #667eea;
                color: white;
                padding: 8px 15px;
                border-radius: 20px;
                font-size: 14px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            
            th {{
                background: #f8f9fa;
                padding: 15px;
                text-align: left;
                font-weight: 600;
                color: #555;
                border-bottom: 2px solid #dee2e6;
            }}
            
            td {{
                padding: 12px 15px;
                border-bottom: 1px solid #dee2e6;
                color: #666;
            }}
            
            tr:hover {{
                background: #f8f9fa;
            }}
            
            @media (max-width: 768px) {{
                .header {{
                    flex-direction: column;
                    text-align: center;
                }}
                
                .header h1 {{
                    font-size: 24px;
                }}
                
                th, td {{
                    padding: 10px;
                    font-size: 14px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <h1>
                    <i class="fas fa-chart-line"></i>
                    Admin Dashboard
                </h1>
                <a href="/admin" class="logout-btn" onclick="sessionStorage.clear()">
                    <i class="fas fa-sign-out-alt"></i>
                    Logout
                </a>
            </div>
            
            <div class="stats-container">
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <div class="stat-info">
                        <h3>Total Candidates</h3>
                        <p>{len(data_store)}</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-calendar-check"></i>
                    </div>
                    <div class="stat-info">
                        <h3>Today's Forms</h3>
                        <p>{today_count}</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-flask"></i>
                    </div>
                    <div class="stat-info">
                        <h3>MLT Course</h3>
                        <p>{mlt_count}</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-x-ray"></i>
                    </div>
                    <div class="stat-info">
                        <h3>GRD Course</h3>
                        <p>{grd_count}</p>
                    </div>
                </div>
            </div>
            
            <div class="table-container">
                <div class="table-header">
                    <h2>
                        <i class="fas fa-list"></i>
                        Candidate Details
                    </h2>
                    <span class="total-count">Total: {len(data_store)} Records</span>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Course</th>
                            <th>Mobile</th>
                            <th>Email</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows if rows else '<tr><td colspan="6" style="text-align: center; padding: 30px;">No data available</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)