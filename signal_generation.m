%% GENERATION OF DISCRETE-TIME SIGNALS
%  ==================================
%  Plots the continuous-time (CT) and discrete-time (DT) forms of five basic
%  signals:
%
%     i.   Step Function        u(t)   /  u[n]
%     ii.  Impulse Function     d(t)   /  d[n]
%     iii. Exponential Function e^(at) /  a^n
%     iv.  Ramp Function        r(t)   /  r[n]
%     v.   Sine Function        sin(wt)/  sin(wn)
%
%  Run:  >> signal_generation

clear; close all; clc;

a = 0.5;            % exponential rate  (0 < a < 1  ->  decaying)
w = pi/4;           % sine angular frequency, rad/sample

t = linspace(-5, 5, 2001);   % continuous-time axis
n = -10:10;                  % discrete-time axis (integers only)

%% i. Step function ----------------------------------------------------------
figure('Name','Step Function');
subplot(1,2,1);
u_t = double(t >= 0);
plot(t, u_t, 'b', 'LineWidth', 2); grid on;
xlabel('t'); ylabel('u(t)'); title('(i-a) Continuous-Time Step  u(t)');
axis([-5 5 -0.3 1.4]); hold on;
plot(0, 0, 'ko', 'MarkerFaceColor', 'w'); hold off;

subplot(1,2,2);
u_n = double(n >= 0);
stem(n, u_n, 'b', 'filled', 'LineWidth', 1.5); grid on;
xlabel('n'); ylabel('u[n]'); title('(i-b) Discrete-Time Step  u[n]');
axis([-10.5 10.5 -0.3 1.4]); hold on;
plot(0, 0, 'ko', 'MarkerFaceColor', 'w'); hold off;

%% ii. Impulse function ------------------------------------------------------
%  The CT impulse d(t) is a Dirac delta: infinite height, zero width, so it is
%  drawn as a unit arrow rather than an ordinary point.
figure('Name','Impulse Function');
subplot(1,2,1);
quiver(0, 0, 0, 1, 0, 'b', 'LineWidth', 2, 'MaxHeadSize', 0.4); grid on;
xlabel('t'); ylabel('d(t)'); title('(ii-a) Continuous-Time Impulse  d(t)');
axis([-5 5 -0.3 1.4]);

subplot(1,2,2);
d_n = double(n == 0);
stem(n, d_n, 'b', 'filled', 'LineWidth', 1.5); grid on;
xlabel('n'); ylabel('d[n]'); title('(ii-b) Discrete-Time Impulse  d[n]');
axis([-10.5 10.5 -0.3 1.4]); hold on;
plot(0, 0, 'ko', 'MarkerFaceColor', 'w'); hold off;

%% iii. Exponential function -------------------------------------------------
figure('Name','Exponential Function');
subplot(1,2,1);
plot(t, exp(a*t), 'b', 'LineWidth', 2); grid on;
xlabel('t'); ylabel('e^{at}'); title('(iii-a) Continuous-Time Exponential  e^{at}');
axis([-5 5 0 exp(a*5)*1.15]); hold on;
plot(0, 0, 'ko', 'MarkerFaceColor', 'w'); hold off;

subplot(1,2,2);
stem(n, a.^n, 'b', 'filled', 'LineWidth', 1.5); grid on;
xlabel('n'); ylabel('a^n'); title('(iii-b) Discrete-Time Exponential  a^n');
axis([-10.5 10.5 0 a^10*1.15]); hold on;
plot(0, 0, 'ko', 'MarkerFaceColor', 'w'); hold off;

%% iv. Ramp function ---------------------------------------------------------
figure('Name','Ramp Function');
subplot(1,2,1);
plot(t, max(t, 0), 'b', 'LineWidth', 2); grid on;
xlabel('t'); ylabel('r(t)'); title('(iv-a) Continuous-Time Ramp  r(t)');
axis([-5 5 -0.4 5.5]); hold on;
plot(0, 0, 'ko', 'MarkerFaceColor', 'w'); hold off;

subplot(1,2,2);
stem(n, max(n, 0), 'b', 'filled', 'LineWidth', 1.5); grid on;
xlabel('n'); ylabel('r[n]'); title('(iv-b) Discrete-Time Ramp  r[n]');
axis([-10.5 10.5 -0.4 11]); hold on;
plot(0, 0, 'ko', 'MarkerFaceColor', 'w'); hold off;

%% v. Sine function ----------------------------------------------------------
figure('Name','Sine Function');
subplot(1,2,1);
plot(t, sin(w*t), 'b', 'LineWidth', 2); grid on;
xlabel('t'); ylabel('sin(wt)'); title('(v-a) Continuous-Time Sine  sin(wt)');
axis([-5 5 -1.4 1.4]); hold on;
plot(0, 0, 'ko', 'MarkerFaceColor', 'w'); hold off;

subplot(1,2,2);
stem(n, sin(w*n), 'b', 'filled', 'LineWidth', 1.5); grid on;
xlabel('n'); ylabel('sin(wn)'); title('(v-b) Discrete-Time Sine  sin(wn)');
axis([-10.5 10.5 -1.4 1.4]); hold on;
plot(0, 0, 'ko', 'MarkerFaceColor', 'w'); hold off;

disp('All five signal plots generated.');