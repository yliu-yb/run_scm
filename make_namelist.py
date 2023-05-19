
def make(run_hours, start_year, start_month, start_day, start_hour, end_year, end_month, end_day, end_hour, bkgrid_res, physic_id):
    file = open("../scm_input/namelist.input", "w")
    config = """&time_control
    run_days                                 = 00,
    run_hours                                = %s,
    run_minutes                              = 00,
    run_seconds                              = 00,
    start_year                               = %s,
    start_month                              = %s,
    start_day                                = %s,
    start_hour                               = %s,
    start_minute                             = 00,
    start_second                             = 00,
    end_year                                 = %s,
    end_month                                = %s,
    end_day                                  = %s,
    end_hour                                 = %s,
    end_minute                               = 00,
    end_second                               = 00,
    history_interval                         = 10,
    frames_per_outfile                       = 100000,
    restart                                  = .false.,
    restart_interval                         = 1440000,
    io_form_history                          = 2,
    io_form_restart                          = 2,
    io_form_input                            = 2,
    io_form_boundary                         = 2,
    auxinput3_inname                         = "force_ideal.nc",
    auxinput3_interval_h                     = 1,
    io_form_auxinput3                        = 2,
    /
    &domains
    time_step                                = %s,
    time_step_fract_num                      = 0,
    time_step_fract_den                      = 1,
    max_dom                                  = 1,
    s_we                                     = 1,
    e_we                                     = 3,
    s_sn                                     = 1,
    e_sn                                     = 3,
    s_vert                                   = 1,
    e_vert                                   = 60,
    dx                                       = %s,
    dy                                       = %s,
    ztop                                     = 19000.,

    /
    &scm
    scm_force                                = 1,
    scm_force_dx                             = %s,
    num_force_layers                         = 72,
    scm_lu_index                             = 2,
    scm_isltyp                               = 4,
    scm_vegfra                               = 0.5,
    scm_lat                                  = 32.74,
    scm_lon                                  = 117.14,
    scm_th_adv                               = .true.,
    scm_wind_adv                             = .true.,
    scm_qv_adv                               = .true.,
    scm_vert_adv                             = .true.,
    /
    &physics
    num_soil_layers                          = 4,
    mp_physics                               = %s,
    ra_lw_physics                            = %s,
    ra_sw_physics                            = %s,
    radt                                     = %s,
    sf_sfclay_physics                        = %s,
    sf_surface_physics                       = %s,
    bl_pbl_physics                           = %s,
    bldt                                     = %s,
    cu_physics                               = %s,
    cudt                                     = %s,
    /
    &dynamics
    hybrid_opt                               = 0,
    rk_ord                                   = 3,
    diff_opt                                 = 1,
    km_opt                                   = 4,
    damp_opt                                 = 3,
    dampcoef                                 = 0.2,
    base_temp                                = 290.,
    zdamp                                    = 5000,
    khdif                                    = 0,
    kvdif                                    = 100,
    smdiv                                    = 0.1,
    emdiv                                    = 0.01,
    epssm                                    = .1,
    time_step_sound                          = 0,
    h_mom_adv_order                          = 5,
    v_mom_adv_order                          = 3,
    h_sca_adv_order                          = 5,
    v_sca_adv_order                          = 3,
    pert_coriolis                            = .true.,
    mix_full_fields                          = .true.,
    non_hydrostatic                          = .true.,
    /
    &bdy_control
    periodic_x                               = .true.,
    symmetric_xs                             = .false.,
    symmetric_xe                             = .false.,
    open_xs                                  = .false.,
    open_xe                                  = .false.,
    periodic_y                               = .true.,
    symmetric_ys                             = .false.,
    symmetric_ye                             = .false.,
    open_ys                                  = .false.,
    open_ye                                  = .false.,
    /
    &namelist_quilt
    nio_tasks_per_group                      = 0,
    nio_groups                               = 1,
    /"""
    mk = True
    mp_physics = 0
    ra_lw_physics = 0
    ra_sw_physics = 0
    radt = 3
    sf_sfclay_physics = 0
    sf_surface_physics = 0
    bl_pbl_physics = 0
    bldt = 0
    cu_physics = 0
    cudt = 0
    physic_id = int(physic_id)
    # physic_id = 6
    if physic_id == 1:
        mp_physics = 9
        ra_lw_physics = 1
        ra_sw_physics = 1
        radt = 3
        sf_sfclay_physics = 2
        sf_surface_physics = 2
        bl_pbl_physics = 2
        bldt = 0
        if bkgrid_res == "3":
            cu_physics = 0
        else:
            cu_physics = 1
        cudt = 0
    elif physic_id == 2:
        mp_physics = 9
        ra_lw_physics = 1
        ra_sw_physics = 1
        radt = 27
        sf_sfclay_physics = 2
        sf_surface_physics = 2
        bl_pbl_physics = 2
        bldt = 0
        cu_physics = 0
        cudt = 0
    elif physic_id == 3:
        mp_physics = 9
        ra_lw_physics = 1
        ra_sw_physics = 1
        radt = 0
        sf_sfclay_physics = 2
        sf_surface_physics = 2
        bl_pbl_physics = 2
        bldt = 0
        cu_physics = 0
        cudt = 0
    elif physic_id == 4:
        mp_physics = 17
        ra_lw_physics = 1
        ra_sw_physics = 1
        radt = 1
        sf_sfclay_physics = 2
        sf_surface_physics = 2
        bl_pbl_physics = 2
        bldt = 0
        cu_physics = 0
        cudt = 0
    elif physic_id == 5:
        mp_physics = 2
        ra_lw_physics = 1
        ra_sw_physics = 1
        radt = 0
        sf_sfclay_physics = 1
        sf_surface_physics = 2
        bl_pbl_physics = 1
        bldt = 0
        cu_physics = 0
        cudt = 0
    elif physic_id == 6:
        mp_physics = 9
        ra_lw_physics = 1
        ra_sw_physics = 1
        radt = 0
        sf_sfclay_physics = 2
        sf_surface_physics = 2
        bl_pbl_physics = 2
        bldt = 0
        cu_physics = 0
        cudt = 0
    elif physic_id == 7:
        mp_physics = 9
        ra_lw_physics = 4
        ra_sw_physics = 4
        radt = 0
        sf_sfclay_physics = 2
        sf_surface_physics = 2
        bl_pbl_physics = 2
        bldt = 0
        cu_physics = 0
        cudt = 0
    print("p_physic:", mp_physics)
    print("cu_physic:", cu_physics)

    config = config % (
        run_hours, start_year, start_month, start_day, start_hour, end_year, end_month, end_day, end_hour,
        int(bkgrid_res) * 6, int(bkgrid_res) * 1000, int(bkgrid_res) * 1000, int(bkgrid_res) * 1000, mp_physics,
        ra_lw_physics, ra_sw_physics, radt, sf_sfclay_physics, sf_surface_physics, bl_pbl_physics, bldt, cu_physics,
        cudt)

    file.writelines(config)
    file.close()
