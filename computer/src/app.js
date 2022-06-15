import React, { useState } from "react";
import { styled, createTheme, ThemeProvider } from "@mui/material/styles";
import { CssBaseline, Box, AppBar, Drawer, Toolbar, Typography, IconButton, Divider, List, Container, Grid, Paper } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";

import SideBar from "./component/sidebar";
import ClockList from "./component/clocklist";
import { TASK } from "./constant";

const client = new WebSocket("ws://localhost:4000");
const drawerWidth = 240;
const sendData = (task, payload = "") => {
    client.send(
        JSON.stringify({
            client: "Frontend",
            task: task,
            payload: payload,
        })
    );
};
client.onopen = (msg) => {
    sendData("init");
};

const NMAppBar = styled(AppBar, {
    shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(["width", "margin"], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    ...(open && {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(["width", "margin"], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    }),
}));
const NMDrawer = styled(Drawer, { shouldForwardProp: (prop) => prop !== "open" })(({ theme, open }) => ({
    "& .MuiDrawer-paper": {
        position: "relative",
        whiteSpace: "nowrap",
        width: drawerWidth,
        transition: theme.transitions.create("width", {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
        boxSizing: "border-box",
        ...(!open && {
            overflowX: "hidden",
            transition: theme.transitions.create("width", {
                easing: theme.transitions.easing.sharp,
                duration: theme.transitions.duration.leavingScreen,
            }),
            width: theme.spacing(7),
            [theme.breakpoints.up("sm")]: {
                width: theme.spacing(9),
            },
        }),
    },
}));
const mdtheme = createTheme();

export default () => {
    const [open, setOpen] = useState(false);
    const [display, setDisplay] = useState("Timer");
    const [timelist, setTimelist] = useState([]);

    const toggleDrawer = () => {
        setOpen(!open);
    };
    const changeDisplay = (state) => {
        setDisplay(display);
    };

    client.onmessage = (mes) => {
        const Mes = mes.data;
        const { task, payload } = JSON.parse(Mes);
        const { success, data } = payload;
        if (!success) {
            // TODO: alert
        } else {
            switch (task) {
                case TASK.GET_TIME_LIST:
                    setTimelist(data);
                    break;
                default:
                    break;
            }
        }
    };

    return (
        <ThemeProvider theme={mdtheme}>
            <Box sx={{ display: "flex" }}>
                <CssBaseline />
                <NMAppBar position="absolute" open={open}>
                    <Toolbar sx={{ pr: "24px" }}>
                        <IconButton
                            edge="start"
                            color="inherit"
                            aria-label="open drawer"
                            onClick={toggleDrawer}
                            sx={{
                                marginRight: "36px",
                                ...(open && { display: "none" }),
                            }}>
                            <MenuIcon />
                        </IconButton>
                        <Typography component="h1" variant="h6" color="inherit" noWrap sx={{ flexGrow: 1 }}>
                            xxMaxiexxBed
                        </Typography>
                    </Toolbar>
                </NMAppBar>
                <NMDrawer variant="permanent" open={open}>
                    <Toolbar
                        sx={{
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "flex-end",
                            px: [1],
                        }}>
                        <IconButton onClick={toggleDrawer}>
                            <ChevronLeftIcon />
                        </IconButton>
                    </Toolbar>
                    <Divider />
                    <List component="nav">
                        <SideBar changeDisplay={changeDisplay} />
                    </List>
                </NMDrawer>
                <Box
                    component="main"
                    sx={{
                        backgroundColor: (theme) => (theme.palette.mode === "light" ? theme.palette.grey[100] : theme.palette.grey[900]),
                        flexGrow: 1,
                        height: "100vh",
                        overflow: "auto",
                    }}>
                    <Toolbar />
                    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                        <Grid container spacing={3}>
                            {/* Clock list */}
                            <Grid item xs={12}>
                                <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
                                    <ClockList timelist={timelist} sendData={sendData} />
                                </Paper>
                            </Grid>
                        </Grid>
                    </Container>
                </Box>
            </Box>
        </ThemeProvider>
    );
};
