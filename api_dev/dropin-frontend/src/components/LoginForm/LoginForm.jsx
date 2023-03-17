import React from "react";

export default function LoginForm({onChange, onSubmit}) {
    return (
        <form onSubmit={(e) => onSubmit(e)}>
            <div className="mb-3">
                <label htmlFor="exampleInputEmail1" className="form-label">Email address</label>
                <input type="email"
                       name="email"
                       className="form-control"
                       id="exampleInputEmail1"
                       aria-describedby="emailHelp"
                       onChange={(e) => onChange(e)}
                />
            </div>
            <div className="mb-3">
                <label htmlFor="exampleInputPassword1" className="form-label">Password</label>
                <input type="password"
                       name="password"
                       className="form-control"
                       id="exampleInputPassword1"
                       onChange={(e) => onChange(e)}
                />
            </div>
            <div className="mb-3 form-check">
                <input type="checkbox" className="form-check-input" id="exampleCheck1"/>
                <label className="form-check-label" htmlFor="exampleCheck1">Remember me</label>
            </div>
            <button type="submit" className="btn btn-primary" >Submit</button>
        </form>
    )
}
