package com.aiy.zoutao_wen.aiyandroidapplication;

public class User {
    protected String id;
    protected String fname;
    protected String lname;
    protected String e_mail;
    protected String user_description;
    protected String role;
    protected String creation_time;
    protected String expiration_time;


    public User(String id, String fname, String lname, String e_mail,
                String user_description, String role, String creation_time,
                String expiration_time) {
        this.id = id;
        this.fname = fname;
        this.lname = lname;
        this.e_mail = e_mail;
        this.user_description = user_description;
        this.role = role;
        this.creation_time = creation_time;
        this.expiration_time = expiration_time;
    }

    public String getId() {
        return id;
    }

    public String getFname() {
        return fname;
    }

    public String getLname() {
        return lname;
    }

    public String getE_mail() {
        return e_mail;
    }

    public String getUser_description() {
        return user_description;
    }

    public String getRole() {
        return role;
    }

    public String getCreation_time() {
        return creation_time;
    }

    public String getExpiration_time() {
        return expiration_time;
    }
}
